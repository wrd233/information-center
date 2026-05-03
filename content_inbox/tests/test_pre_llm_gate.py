from app.models import NormalizedContent
from app.processor import _collect_hints, pre_llm_gate


def _make_content(title="", summary="", content_text=""):
    return NormalizedContent(
        title=title,
        url=None,
        source_name="test",
        source_category=None,
        content_type="article",
        published_at=None,
        author=None,
        summary=summary,
        content_text=content_text,
        guid=None,
    )


class TestPreLlmGate:
    def test_empty_content_skips_llm(self):
        nc = _make_content(title="", summary="", content_text="")
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is False
        assert reason == "empty_content"

    def test_too_short_skips_llm(self):
        nc = _make_content(title="好", summary="不错", content_text="")
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is False
        assert reason == "too_short"

    def test_normal_content_passes(self):
        nc = _make_content(
            title="DeepSeek 发布新模型",
            summary="DeepSeek 今天发布了新一代大语言模型，性能大幅提升...",
            content_text="详细内容介绍...",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True
        assert reason == ""

    def test_short_title_with_body_passes(self):
        nc = _make_content(
            title="AI",
            summary="这是一篇关于人工智能的长文摘要，包含了很多有价值的信息和观点，值得一读。文章讨论了最新进展和趋势。",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True

    def test_ad_keyword_does_not_block(self):
        nc = _make_content(
            title="限时优惠！AI 课程大促销",
            summary="某平台推出了限时优惠活动，AI 课程降价50%，内容涵盖深度学习...",
            content_text="详细描述课程内容和优惠信息，以及课程大纲...",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True
        assert "possible_ad" in hints

    def test_job_keyword_does_not_block(self):
        nc = _make_content(
            title="招聘 AI 工程师",
            summary="某大厂招聘 AI 工程师，要求硕士以上学历，熟悉大模型训练...",
            content_text="详细岗位描述，包括工作内容和团队介绍...",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True
        assert "possible_job" in hints

    def test_digest_keyword_does_not_block(self):
        nc = _make_content(
            title="AI 周报第 42 期",
            summary="本周 AI 领域的重要进展汇总，包括多个新产品发布...",
            content_text="详细汇总内容，涵盖 OpenAI、DeepSeek 等动态...",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True
        assert "possible_digest" in hints

    def test_navigation_keyword_does_not_block(self):
        nc = _make_content(
            title="AI 资源汇总",
            summary="汇总了最近一个月 AI 相关的工具和资源链接...",
            content_text="GitHub 链接、论文链接等资源列表...",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True
        assert "possible_navigation" in hints

    def test_no_hints_for_normal_title(self):
        nc = _make_content(
            title="深入理解 Transformer 架构",
            summary="详细介绍 Transformer 架构的设计原理...",
            content_text="详细技术文章内容...",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True
        assert hints == []

    def test_empty_title_with_body_passes(self):
        nc = _make_content(
            title="",
            summary="这是一段足够长的摘要，包含了文章的主要内容概述，介绍了这个话题的核心观点和关键信息。",
        )
        should_call, reason, hints = pre_llm_gate(nc)
        assert should_call is True


class TestCollectHints:
    def test_ad_hints(self):
        assert "possible_ad" in _collect_hints("限时优惠！")

    def test_job_hints(self):
        assert "possible_job" in _collect_hints("急招 AI 工程师")

    def test_multiple_hints(self):
        hints = _collect_hints("招聘内推 | 限时优惠")
        assert "possible_ad" in hints
        assert "possible_job" in hints
