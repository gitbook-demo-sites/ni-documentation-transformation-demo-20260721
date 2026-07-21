import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
BASE = "https://api.gitbook.com/v1"
ORG_ID = "awML61cx1m4WXZ7SRY3D"
SITE_ID = "site_RfSEz"
PRIVATE_REPO = "louissteen/ni-docs-gitbook-2"
PUBLIC_OWNER = "gitbook-demo-sites"
PUBLIC_REPO = "ni-documentation-transformation-demo-20260721"
PUBLIC_URL = f"https://github.com/{PUBLIC_OWNER}/{PUBLIC_REPO}.git"
RAW = f"https://raw.githubusercontent.com/{PUBLIC_OWNER}/{PUBLIC_REPO}/main"


SPACES = [
    {
        "key": "HOME",
        "sentinel": "XSPACE_HOME",
        "folder": "home",
        "title": "Home",
        "emoji": "1f3e0",
        "icon": "house",
        "path": "home",
        "description": "Executive entry point for the NI documentation transformation demo.",
    },
    {
        "key": "AUTHORING",
        "sentinel": "XSPACE_AUTHORING",
        "folder": "authoring",
        "title": "Authoring & contribution",
        "emoji": "270d-fe0f",
        "icon": "pen-to-square",
        "path": "authoring",
        "description": "Markdown, DITA migration choices, SME reviews, agency contribution, and GitHub workflows.",
    },
    {
        "key": "DELIVERY",
        "sentinel": "XSPACE_DELIVERY",
        "folder": "delivery",
        "title": "Delivery & localization",
        "emoji": "1f30d",
        "icon": "language",
        "path": "delivery",
        "description": "Online HTML delivery, metadata, gated/public publishing, PDF continuity, and TMS integration.",
    },
    {
        "key": "AI",
        "sentinel": "XSPACE_AI",
        "folder": "ai-automation",
        "title": "AI & automation",
        "emoji": "1f916",
        "icon": "sparkles",
        "path": "ai-automation",
        "description": "AI drafting, AI search, content operations automation, and metrics for documentation velocity.",
    },
]


def run(cmd, **kwargs):
    subprocess.run(cmd, cwd=ROOT, check=True, **kwargs)


def write(path: str, content: str) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def api(method: str, path: str, body=None, expected=(200, 201, 204)):
    token = os.environ["GITBOOK_TOKEN"]
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            text = resp.read().decode()
            payload = json.loads(text) if text else None
            if resp.status not in expected:
                raise RuntimeError(f"{method} {path} returned {resp.status}: {text}")
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"{method} {path} returned {exc.code}: {detail}") from exc


def yaml_file(space: str) -> None:
    write(
        f"{space}/.gitbook.yaml",
        """
        root: ./
        structure:
          readme: README.md
          summary: SUMMARY.md
        """,
    )


def vars_file(space: str) -> None:
    write(
        f"{space}/.gitbook/vars.yaml",
        """
        company_name: National Instruments
        parent_company: Emerson
        demo_name: NI Documentation Transformation Demo
        current_cms: DITA in Oracle
        incumbent_delivery: Zoomin
        priority_scope: Software documentation first
        writer_count: "24"
        content_estate: "300,000 pages and 2,500+ manuals"
        """,
    )


def summary(space: str, lines: list[str]) -> None:
    write(f"{space}/SUMMARY.md", "# Table of contents\n\n" + "\n".join(lines))


def scaffold_assets() -> None:
    write(
        "assets/ni-wordmark.svg",
        """
        <svg xmlns="http://www.w3.org/2000/svg" width="520" height="96" viewBox="0 0 520 96" role="img" aria-label="NI">
          <rect width="520" height="96" rx="8" fill="#111827"/>
          <rect x="24" y="24" width="86" height="48" rx="2" fill="#F5C400"/>
          <text x="38" y="60" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="800" fill="#111827">NI</text>
          <text x="134" y="58" font-family="Arial, Helvetica, sans-serif" font-size="29" font-weight="700" fill="#FFFFFF">Documentation Hub</text>
          <text x="136" y="78" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#CBD5E1">by Emerson</text>
        </svg>
        """,
    )
    write(
        "assets/ni-cover.svg",
        """
        <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="540" viewBox="0 0 1600 540" role="img" aria-label="NI Documentation Transformation Demo">
          <rect width="1600" height="540" fill="#111827"/>
          <rect x="0" y="0" width="1600" height="14" fill="#F5C400"/>
          <rect x="88" y="88" width="500" height="324" rx="10" fill="#F8FAFC"/>
          <rect x="126" y="126" width="90" height="54" rx="3" fill="#F5C400"/>
          <text x="143" y="164" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="800" fill="#111827">NI</text>
          <rect x="126" y="216" width="380" height="18" rx="9" fill="#111827"/>
          <rect x="126" y="260" width="316" height="12" rx="6" fill="#94A3B8"/>
          <rect x="126" y="290" width="356" height="12" rx="6" fill="#CBD5E1"/>
          <rect x="126" y="344" width="142" height="48" rx="4" fill="#111827"/>
          <rect x="290" y="344" width="142" height="48" rx="4" fill="#F5C400"/>
          <g fill="none" stroke="#F5C400" stroke-width="4" opacity=".9">
            <path d="M824 160 H1030 V98 H1260"/>
            <path d="M824 270 H1090"/>
            <path d="M824 382 H1030 V446 H1260"/>
          </g>
          <g fill="#F5C400">
            <circle cx="824" cy="160" r="12"/>
            <circle cx="824" cy="270" r="12"/>
            <circle cx="824" cy="382" r="12"/>
            <circle cx="1260" cy="98" r="12"/>
            <circle cx="1090" cy="270" r="12"/>
            <circle cx="1260" cy="446" r="12"/>
          </g>
          <text x="734" y="220" font-family="Arial, Helvetica, sans-serif" font-size="64" font-weight="800" fill="#FFFFFF">Future-state docs</text>
          <text x="738" y="272" font-family="Arial, Helvetica, sans-serif" font-size="27" fill="#CBD5E1">Open contribution, AI drafting, HTML delivery,</text>
          <text x="738" y="310" font-family="Arial, Helvetica, sans-serif" font-size="27" fill="#CBD5E1">metadata enrichment, and translation-ready workflows.</text>
        </svg>
        """,
    )


def scaffold_home() -> None:
    write(
        "home/README.md",
        f"""
        ---
        description: "A GitBook proof-of-concept for NI's future documentation platform."
        icon: house
        cover: "{RAW}/assets/ni-cover.svg"
        coverY: 0
        layout:
          width: wide
          cover:
            visible: true
            size: hero
          title:
            visible: true
          description:
            visible: true
          tableOfContents:
            visible: false
          outline:
            visible: false
          pagination:
            visible: true
        ---

        # NI Documentation Transformation Demo

        A tailored GitBook sandbox for National Instruments, focused on the software-documentation slice of a larger CMS transformation.

        This first draft borrows the product-catalog feel of the SICK demo, then adapts it to NI's actual evaluation themes: moving from DITA in Oracle, replacing Zoomin, opening contribution through GitHub, keeping translation non-negotiable, and giving writers an AI-native workflow.

        {{% columns %}}
        {{% column width="64%" %}}
        <button type="button" class="button primary" data-action="ask" data-icon="gitbook-assistant">Ask the NI docs transformation demo...</button>

        <button type="button" class="button secondary" data-action="ask" data-query="How would GitBook support NI's TMS workflow?" data-icon="language">TMS workflow</button> <button type="button" class="button secondary" data-action="ask" data-query="How can SMEs contribute through GitHub?" data-icon="code-branch">Open contribution</button> <button type="button" class="button secondary" data-action="ask" data-query="What is the path from DITA to Markdown?" data-icon="diagram-project">DITA to Markdown</button> <button type="button" class="button secondary" data-action="ask" data-query="How does GitBook improve authoring velocity?" data-icon="sparkles">AI authoring</button>
        {{% endcolumn %}}

        {{% column width="36%" %}}
        {{% hint style="info" icon="gitbook" %}}
        **This is a discovery-driven sandbox.** It uses a small representative content set to show the future-state operating model, not to migrate NI's full 300,000-page estate.
        {{% endhint %}}
        {{% endcolumn %}}
        {{% endcolumns %}}

        ***

        ## Choose a transformation path

        <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        <tr><td><h3><i class="fa-pen-to-square" style="color:$primary;">:pen:</i></h3></td><td><strong>Author and contribute</strong></td><td>How writers, SMEs, agencies, and customers can collaborate through Markdown, pull requests, review workflows, and AI drafting.</td><td><a href="https://app.gitbook.com/s/XSPACE_AUTHORING/">Authoring</a></td></tr>
        <tr><td><h3><i class="fa-language" style="color:$primary;">:language:</i></h3></td><td><strong>Deliver and localize</strong></td><td>How GitBook supports online HTML delivery, metadata, gated/public publishing, PDF continuity, and translation handoffs.</td><td><a href="https://app.gitbook.com/s/XSPACE_DELIVERY/">Delivery</a></td></tr>
        <tr><td><h3><i class="fa-sparkles" style="color:$primary;">:sparkles:</i></h3></td><td><strong>Automate with AI</strong></td><td>Where AI search, drafting, content checks, MCP access, and metrics reduce authoring friction and increase velocity.</td><td><a href="https://app.gitbook.com/s/XSPACE_AI/">AI</a></td></tr>
        </tbody></table>

        ## Why this matters for NI

        {{% columns %}}
        {{% column %}}
        ### Current-state friction

        * DITA content is stored in Oracle and hard to access directly.
        * Zoomin is going away, creating a forced delivery-platform decision.
        * The team needs public and gated publishing, without losing legacy PDF paths.
        * Translation is mandatory and already depends on a mature TMS with APIs.
        {{% endcolumn %}}

        {{% column %}}
        ### Future-state signal

        * Git-backed docs give writers, SMEs, and agencies a familiar contribution path.
        * Markdown unlocks AI-assisted authoring without blocking a DITA transition path.
        * Metadata-rich HTML improves search, AI answers, and customer navigation.
        * GitBook can show a practical alternative to a costly in-house rebuild.
        {{% endcolumn %}}
        {{% endcolumns %}}

        ```mermaid
        flowchart LR
            DITA[DITA in Oracle] --> Export[DITA to Markdown export]
            Export --> GitHub[GitHub repository]
            GitHub --> Review[SME and writer review]
            Review --> GitBook[GitBook spaces]
            GitBook --> HTML[Online HTML delivery]
            GitBook --> TMS[Translation management system]
            GitBook --> AI[AI search and drafting]
        ```
        """,
    )
    summary(
        "home",
        [
            "* [NI Documentation Transformation Demo](README.md)",
            "* [Demo scope and assumptions](demo-scope.md)",
            "* [Future-state operating model](operating-model.md)",
        ],
    )
    write(
        "home/demo-scope.md",
        """
        ---
        description: "What this first draft includes, what it assumes, and where solution engineering should go deeper."
        icon: clipboard-check
        ---

        # Demo scope and assumptions

        This sandbox focuses on software documentation first, because that is the lower-governance entry point discussed on the discovery call. Hardware manuals, regulated safety content, and deep DITA specialization can remain in the current CMS while the team validates the Git-backed software path.

        {% hint style="warning" icon="triangle-exclamation" %}
        The source repository provided for this build was empty at the time of generation, so the first draft uses the discovery summary, the public NI site, and the SICK sandbox structure as the content model.
        {% endhint %}

        ## Included in this draft

        * A future-state homepage modeled after the SICK catalog-style demo.
        * A contribution model for writers, SMEs, agencies, and possible customer pull requests.
        * A translation workflow that keeps the existing TMS as the system of record.
        * A sample AI authoring and automation workflow for velocity KPIs.

        ## Not included yet

        * Real NI DITA XML or converted Markdown samples.
        * Direct integration details for NI's actual translation management system.
        * Hardware-manual governance flows.
        * A side-by-side Docusaurus CX comparison.
        """,
    )
    write(
        "home/operating-model.md",
        """
        ---
        description: "A practical operating model for a Git-backed documentation program at NI."
        icon: diagram-project
        ---

        # Future-state operating model

        The operating model is designed around one principle: content should be easy for humans and agents to access, review, reuse, translate, and publish.

        {% stepper %}
        {% step %}
        ### Convert or export source content

        Start with NI's existing DITA-to-Markdown export for software docs. Keep DITA as a source option while the team decides whether Markdown becomes the authoring format or the publish-time format.
        {% endstep %}

        {% step %}
        ### Review in GitHub

        Writers, SMEs, external agencies, and approved customer contributors propose changes through branches and pull requests. CODEOWNERS can route reviews by product area.
        {% endstep %}

        {% step %}
        ### Publish through GitBook

        GitBook turns the reviewed source into searchable HTML with metadata, page feedback, AI answers, and public or gated visibility.
        {% endstep %}

        {% step %}
        ### Localize through the TMS

        Export changed content and metadata to the existing translation management system, then import localized content back into the Git/GitBook workflow.
        {% endstep %}
        {% endstepper %}
        """,
    )


def scaffold_authoring() -> None:
    write(
        "authoring/README.md",
        """
        ---
        description: "A Git-backed contribution model for writers, SMEs, agencies, and customers."
        icon: pen-to-square
        layout:
          width: wide
          title:
            visible: true
          description:
            visible: true
          outline:
            visible: false
        ---

        # Authoring & contribution

        NI's authoring challenge is not just format conversion. It is access. DITA stored in Oracle makes it hard for AI systems, SMEs, agencies, and customer contributors to participate directly.

        <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        <tr><td><h3><i class="fa-file-code" style="color:$primary;">:file_code:</i></h3></td><td><strong>DITA to Markdown strategy</strong></td><td>Choose between full Markdown authoring and DITA-to-Markdown as a publishing pipeline.</td><td><a href="dita-to-markdown.md">DITA strategy</a></td></tr>
        <tr><td><h3><i class="fa-code-branch" style="color:$primary;">:code_branch:</i></h3></td><td><strong>GitHub contribution workflow</strong></td><td>Give SMEs, agencies, and approved external contributors a governed path to propose changes.</td><td><a href="github-contribution-workflow.md">Contribution workflow</a></td></tr>
        <tr><td><h3><i class="fa-users-gear" style="color:$primary;">:users_gear:</i></h3></td><td><strong>Roles and review model</strong></td><td>Map writers, SMEs, localization, and doc services into a clear approval flow.</td><td><a href="roles-and-review.md">Roles</a></td></tr>
        </tbody></table>

        ## Content lifecycle

        ```mermaid
        sequenceDiagram
            participant Writer
            participant AI as AI drafting
            participant SME
            participant GitHub
            participant GitBook

            Writer->>AI: Draft or refactor topic
            AI-->>Writer: Markdown proposal
            Writer->>GitHub: Open pull request
            GitHub->>SME: Request review
            SME-->>GitHub: Approve or comment
            GitHub->>GitBook: Merge to main
            GitBook-->>Writer: Published HTML and AI-indexed content
        ```
        """,
    )
    summary(
        "authoring",
        [
            "* [Authoring & contribution](README.md)",
            "## Migration strategy",
            "* [DITA to Markdown strategy](dita-to-markdown.md)",
            "* [Content repository model](content-repository-model.md)",
            "## Collaboration",
            "* [GitHub contribution workflow](github-contribution-workflow.md)",
            "* [Roles and review model](roles-and-review.md)",
        ],
    )
    write(
        "authoring/dita-to-markdown.md",
        """
        ---
        description: "Compare full Markdown authoring with a DITA-to-Markdown publishing pipeline."
        icon: file-code
        ---

        # DITA to Markdown strategy

        NI has already tested DITA's XML-to-Markdown export, and some content already exists in GitHub-flavored Markdown. That creates two viable paths.

        | Decision | Full Markdown authoring | DITA-to-Markdown publishing pipeline |
        | --- | --- | --- |
        | Best for | New software docs, fast iteration, AI drafting | Legacy content, hardware governance, phased migration |
        | Writer experience | Simple editing in GitBook or GitHub | Writers continue in DITA until migration timing is clear |
        | AI access | Direct access to clean Markdown | AI works on exported Markdown after transformation |
        | Translation impact | TMS integrates with GitBook/GitHub source | TMS can continue receiving structured export outputs |
        | Risk | Requires authoring change management | Adds pipeline complexity and possible transform drift |

        {% hint style="success" icon="lightbulb" %}
        A practical demo path is hybrid: start software docs in Markdown where the team wants velocity, keep DITA-to-Markdown for legacy and hardware content until governance requirements are settled.
        {% endhint %}
        """,
    )
    write(
        "authoring/content-repository-model.md",
        """
        ---
        description: "A repository structure that supports multiple product areas without forcing one giant docs tree."
        icon: folder-tree
        ---

        # Content repository model

        A future repository can mirror NI's product taxonomy without forcing every manual into one navigation tree.

        ```
        ni-docs/
          software/
            labview/
            teststand/
            flexlogger/
            instrumentstudio/
          shared/
            authoring-guides/
            style-guide/
            metadata/
          localization/
            handoff-manifests/
            returned-translations/
        ```

        ## Why this structure helps

        * Product teams can own their folders.
        * Shared guidance lives once and is referenced across products.
        * GitHub CODEOWNERS can request the right SMEs automatically.
        * Translation jobs can be generated from changed files instead of full manuals.
        """,
    )
    write(
        "authoring/github-contribution-workflow.md",
        """
        ---
        description: "How SMEs, agencies, and external contributors can propose documentation updates safely."
        icon: code-branch
        ---

        # GitHub contribution workflow

        Open contribution was one of the clearest objectives from discovery. GitBook can keep the contribution interface approachable while GitHub provides the governance layer underneath.

        {% stepper %}
        {% step %}
        ### Contributor proposes a change

        A writer, SME, agency partner, or approved external contributor edits a Markdown page and opens a pull request.
        {% endstep %}

        {% step %}
        ### Automation checks the change

        Checks validate frontmatter, broken links, required metadata, terminology, and TMS readiness.
        {% endstep %}

        {% step %}
        ### Review routes to the right owner

        CODEOWNERS requests product SMEs, localization, or documentation services depending on file path and metadata.
        {% endstep %}

        {% step %}
        ### Merge publishes the update

        GitBook syncs the merged change and updates the HTML site, AI index, llms files, and page metadata.
        {% endstep %}
        {% endstepper %}
        """,
    )
    write(
        "authoring/roles-and-review.md",
        """
        ---
        description: "A first-pass role model for a 24-writer documentation organization with many SMEs."
        icon: users-gear
        ---

        # Roles and review model

        NI's writers work with many SMEs across multiple projects. The review model should reduce coordination overhead instead of adding another queue.

        | Role | Primary responsibility | GitBook/GitHub workflow |
        | --- | --- | --- |
        | Writer | Draft, structure, and maintain docs | Owns branch and page changes |
        | SME | Validate technical accuracy | Reviews product-specific pull requests |
        | Documentation services | Own templates, metadata, governance | Owns required metadata and publishing standards |
        | Localization lead | Ensure TMS readiness | Reviews translation manifests and localized outputs |
        | External agency | Contribute content at scale | Works in scoped folders with review gates |

        {% hint style="info" icon="route" %}
        For the demo, show a software writer updating a TestStand page, an SME approving it, and a localization check creating a TMS-ready manifest.
        {% endhint %}
        """,
    )


def scaffold_delivery() -> None:
    write(
        "delivery/README.md",
        """
        ---
        description: "Online delivery, metadata, public/gated access, and localization workflows."
        icon: language
        layout:
          width: wide
          title:
            visible: true
          description:
            visible: true
          outline:
            visible: false
        ---

        # Delivery & localization

        NI needs a new delivery model because Zoomin is going away, but delivery cannot be treated separately from translation, metadata, PDFs, and public versus gated access.

        <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        <tr><td><h3><i class="fa-globe" style="color:$primary;">:globe:</i></h3></td><td><strong>HTML delivery model</strong></td><td>Deliver public and gated content with metadata, AI search, page feedback, and generated agent-readable files.</td><td><a href="html-delivery-model.md">HTML delivery</a></td></tr>
        <tr><td><h3><i class="fa-language" style="color:$primary;">:language:</i></h3></td><td><strong>TMS integration path</strong></td><td>Keep the existing translation management system central while GitBook owns publishing and review experience.</td><td><a href="tms-integration-path.md">TMS integration</a></td></tr>
        <tr><td><h3><i class="fa-file-pdf" style="color:$primary;">:file_pdf:</i></h3></td><td><strong>Legacy PDFs and governance</strong></td><td>Maintain PDF continuity for legacy manuals and governed hardware workflows during a phased transition.</td><td><a href="pdf-and-governance.md">PDFs</a></td></tr>
        </tbody></table>
        """,
    )
    summary(
        "delivery",
        [
            "* [Delivery & localization](README.md)",
            "## Publishing",
            "* [HTML delivery model](html-delivery-model.md)",
            "* [Metadata and taxonomy](metadata-and-taxonomy.md)",
            "* [PDFs and governance](pdf-and-governance.md)",
            "## Localization",
            "* [TMS integration path](tms-integration-path.md)",
        ],
    )
    write(
        "delivery/html-delivery-model.md",
        """
        ---
        description: "A replacement delivery model for public and gated NI documentation."
        icon: globe
        ---

        # HTML delivery model

        GitBook can replace the delivery layer with an HTML-first site that is easier to search, easier for agents to read, and easier for writers to improve.

        ## Delivery capabilities to demonstrate

        * Public documentation for most software topics.
        * Gated or role-based content for customer-only assets.
        * Page metadata for product, version, lifecycle stage, audience, and translation state.
        * Page feedback and edit workflows for continuous improvement.
        * AI Assistant, Markdown export, and MCP-friendly access for agent workflows.

        {% hint style="info" icon="lock" %}
        Gated content can be positioned as a positive signal: NI already has public and private information needs, and GitBook can support authenticated access without making the entire docs estate private.
        {% endhint %}
        """,
    )
    write(
        "delivery/metadata-and-taxonomy.md",
        """
        ---
        description: "A first-pass metadata model for NI software documentation."
        icon: tags
        ---

        # Metadata and taxonomy

        Online HTML delivery should enrich content with metadata that helps search, AI answers, governance, and translation.

        | Field | Example | Why it matters |
        | --- | --- | --- |
        | Product | LabVIEW, TestStand, FlexLogger | Routes content ownership and search facets |
        | Content type | Concept, task, reference, release note | Improves navigation and AI retrieval |
        | Audience | Developer, test engineer, admin, customer-only | Supports conditional access and personalization |
        | Source format | Markdown, DITA export, DITA source | Makes migration state visible |
        | Translation state | Source changed, in translation, localized | Keeps localization and publishing aligned |

        ```mermaid
        flowchart TD
            Page[Markdown page] --> Metadata[Metadata frontmatter]
            Metadata --> Search[Search facets]
            Metadata --> AI[AI retrieval context]
            Metadata --> TMS[Translation job manifest]
            Metadata --> Governance[Review ownership]
        ```
        """,
    )
    write(
        "delivery/tms-integration-path.md",
        """
        ---
        description: "How GitBook can coexist with NI's existing translation management system."
        icon: language
        ---

        # TMS integration path

        Translation is non-negotiable for NI, and the current TMS already has rich APIs. The right demo should not suggest replacing it. It should show GitBook as the authoring and delivery layer around it.

        {% stepper %}
        {% step %}
        ### Detect changed source

        A merge to the main branch identifies changed pages, metadata, and assets since the last translation batch.
        {% endstep %}

        {% step %}
        ### Generate a translation manifest

        Automation creates a manifest with source file, product, locale targets, content type, owner, and priority.
        {% endstep %}

        {% step %}
        ### Send to the TMS API

        The manifest and source files are submitted to NI's translation system. The TMS remains the system of record for translation memory and vendor workflow.
        {% endstep %}

        {% step %}
        ### Import localized output

        Returned translations are committed back into Git, reviewed when needed, and published through GitBook.
        {% endstep %}
        {% endstepper %}

        {% hint style="success" icon="plug" %}
        The demo angle: GitBook does not need to own translation memory. It needs to make source changes, metadata, review, and publishing easy to integrate with the TMS NI already trusts.
        {% endhint %}
        """,
    )
    write(
        "delivery/pdf-and-governance.md",
        """
        ---
        description: "Maintain legacy PDF and hardware governance paths while software docs move faster."
        icon: file-pdf
        ---

        # PDFs and governance

        PDFs still matter for legacy content and governed hardware manuals. The first software-docs phase should not require NI to solve every hardware dependency at once.

        ## Suggested phased approach

        * Keep governed hardware content in the existing CMS until review and safety requirements are mapped.
        * Move software docs and less governed content into Git-backed workflows first.
        * Preserve legacy PDF links for customer expectations.
        * Use metadata to show which content is source-authored in Markdown, exported from DITA, or still externally governed.
        """,
    )


def scaffold_ai() -> None:
    write(
        "ai-automation/README.md",
        """
        ---
        description: "AI drafting, AI search, MCP access, automation, and metrics for NI's documentation program."
        icon: sparkles
        layout:
          width: wide
          title:
            visible: true
          description:
            visible: true
          outline:
            visible: false
        ---

        # AI & automation

        NI's KPI is not just better docs. It is more content and faster content. AI and automation should be connected to measurable writer velocity, review cycle time, and findability.

        <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
        <tr><td><h3><i class="fa-wand-magic-sparkles" style="color:$primary;">:sparkles:</i></h3></td><td><strong>AI drafting workflow</strong></td><td>Use AI to generate first drafts, refactor legacy topics, and create reviewer-ready Markdown.</td><td><a href="ai-drafting-workflow.md">AI drafting</a></td></tr>
        <tr><td><h3><i class="fa-magnifying-glass-chart" style="color:$primary;">:mag:</i></h3></td><td><strong>AI search and agent access</strong></td><td>Give engineers, customers, and support teams answers across product docs, release notes, and source content.</td><td><a href="ai-search-and-agents.md">AI search</a></td></tr>
        <tr><td><h3><i class="fa-chart-line" style="color:$primary;">:chart:</i></h3></td><td><strong>Velocity metrics</strong></td><td>Track content quantity, creation speed, review time, translation lag, and AI answer quality.</td><td><a href="velocity-metrics.md">Metrics</a></td></tr>
        </tbody></table>
        """,
    )
    summary(
        "ai-automation",
        [
            "* [AI & automation](README.md)",
            "## Authoring acceleration",
            "* [AI drafting workflow](ai-drafting-workflow.md)",
            "* [Automation checks](automation-checks.md)",
            "## Findability",
            "* [AI search and agents](ai-search-and-agents.md)",
            "* [Velocity metrics](velocity-metrics.md)",
        ],
    )
    write(
        "ai-automation/ai-drafting-workflow.md",
        """
        ---
        description: "A writer-centered AI workflow for creating more content faster."
        icon: wand-magic-sparkles
        ---

        # AI drafting workflow

        AI should help NI writers move from source material to reviewable content faster, without bypassing SME accountability.

        {% tabs %}
        {% tab title="New topic" %}
        1. Writer provides product notes, acceptance criteria, and target audience.
        2. AI drafts a concept, task, or reference page in GitBook-flavored Markdown.
        3. Writer edits tone, metadata, examples, and scope.
        4. SME reviews the pull request.
        {% endtab %}

        {% tab title="Legacy topic" %}
        1. Export DITA topic to Markdown.
        2. AI normalizes headings, links, callouts, and metadata.
        3. Writer checks technical context and removes migration artifacts.
        4. Automation validates broken links and TMS readiness.
        {% endtab %}

        {% tab title="Release note" %}
        1. Product change is summarized from issue, PR, or release notes.
        2. AI creates customer-facing copy with impact and upgrade guidance.
        3. Owner confirms version, affected products, and localization priority.
        {% endtab %}
        {% endtabs %}
        """,
    )
    write(
        "ai-automation/automation-checks.md",
        """
        ---
        description: "Automated quality gates for Git-backed NI documentation."
        icon: list-check
        ---

        # Automation checks

        Automation should make review safer and faster.

        | Check | Purpose |
        | --- | --- |
        | Required metadata | Ensures product, audience, locale, source format, and owner are present |
        | Broken links | Catches moved pages and stale external references |
        | Terminology | Flags off-brand terms and inconsistent product naming |
        | Translation readiness | Finds non-translatable fragments, missing alt text, and unapproved variables |
        | AI summary | Adds a PR summary for reviewers and localization teams |

        {% hint style="info" icon="robot" %}
        The strongest automation story for NI is practical: reduce manual coordination across 24 writers and many SMEs, without asking writers to become platform engineers.
        {% endhint %}
        """,
    )
    write(
        "ai-automation/ai-search-and-agents.md",
        """
        ---
        description: "Search and agent workflows across NI's public and gated content."
        icon: magnifying-glass-chart
        ---

        # AI search and agents

        NI has no AI search today. GitBook can show what changes when documentation is accessible as structured Markdown and HTML instead of being trapped inside a database-backed DITA system.

        ## Demo questions

        * "What is the fastest path to update a software topic and send it to translation?"
        * "Which content should remain in DITA during the first phase?"
        * "How do SMEs propose a change through GitHub?"
        * "What metadata should each software page include?"

        ## Agent-ready outputs

        * Markdown page access.
        * AI Assistant on every page.
        * MCP-friendly access for connected tools.
        * Page-level metadata that improves retrieval context.
        """,
    )
    write(
        "ai-automation/velocity-metrics.md",
        """
        ---
        description: "KPIs for content quantity, velocity, review, localization, and AI quality."
        icon: chart-line
        layout:
          width: wide
        ---

        # Velocity metrics

        The discovery call named two core KPIs: increase quantity of content produced and increase velocity of content creation.

        {% updates format="full" %}
        {% update date="2026-07-21" tags="authoring,ai" %}
        ## AI-assisted draft cycle

        Measure median time from source material to first reviewer-ready draft, split by new topic, legacy migration, and release note.
        {% endupdate %}

        {% update date="2026-07-21" tags="review" %}
        ## SME review cycle

        Track time from pull request opened to SME approval, plus number of review rounds by product area.
        {% endupdate %}

        {% update date="2026-07-21" tags="localization" %}
        ## Translation lag

        Track time from source merge to localized publish by locale, TMS job, and priority.
        {% endupdate %}
        {% endupdates %}
        """,
    )
    write(
        "ai-automation/.gitbook/tags.yaml",
        """
        - tag: authoring
          label: Authoring
          icon: pen-to-square
        - tag: ai
          label: AI
          icon: sparkles
        - tag: review
          label: Review
          icon: user-check
        - tag: localization
          label: Localization
          icon: language
        """,
    )


def scaffold_all() -> None:
    scaffold_assets()
    for item in SPACES:
        yaml_file(item["folder"])
        vars_file(item["folder"])
    scaffold_home()
    scaffold_authoring()
    scaffold_delivery()
    scaffold_ai()
    write(
        "README.md",
        """
        # NI documentation transformation demo

        Source content for the NI GitBook demo site. Each top-level folder is a GitBook space.

        The private source repo is `louissteen/ni-docs-gitbook-2`. A public mirror is used only for GitBook's one-time import path.
        """,
    )
    write(
        ".gitignore",
        """
        .DS_Store
        Thumbs.db
        *.swp
        *.swo
        .idea/
        .vscode/
        gitbook-publish-share.json
        gitbook-import-results.json
        gitbook-created.json
        """,
    )


def git_commit_push() -> None:
    run(["git", "add", "."])
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if result.returncode != 0:
        run(["git", "commit", "-m", "Build NI documentation transformation demo"])
    run(["git", "push", "-u", "origin", "main"])


def push_public_mirror() -> None:
    exists = subprocess.run(
        ["gh", "repo", "view", f"{PUBLIC_OWNER}/{PUBLIC_REPO}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if exists.returncode != 0:
        run(["gh", "repo", "create", f"{PUBLIC_OWNER}/{PUBLIC_REPO}", "--public", "--source", str(ROOT), "--remote", "public", "--push"])
    else:
        remotes = subprocess.run(["git", "remote"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
        if "public" not in remotes:
            run(["git", "remote", "add", "public", PUBLIC_URL])
        run(["git", "push", "public", "main"])


def create_gitbook_objects() -> dict:
    api("PATCH", f"/orgs/{ORG_ID}/sites/{SITE_ID}", {"type": "ultimate", "title": "NI Documentation Transformation Demo", "visibility": "share-link", "basename": "ni-documentation-transformation-demo"})
    created = {"site": SITE_ID, "spaces": {}, "sections": {}, "site_spaces": {}}
    _, current = api("GET", f"/orgs/{ORG_ID}/sites/{SITE_ID}/structure")
    existing_by_title = {
        section.get("title"): section
        for section in current.get("structure", [])
        if section.get("object") == "site-section" and section.get("siteSpaces")
    }
    for item in SPACES:
        existing = existing_by_title.get(item["title"])
        if existing:
            created["sections"][item["key"]] = existing["id"]
            created["site_spaces"][item["key"]] = existing["siteSpaces"][0]["id"]
            created["spaces"][item["key"]] = existing["siteSpaces"][0]["space"]["id"]
            continue
        _, space = api(
            "POST",
            f"/orgs/{ORG_ID}/spaces",
            {"title": item["title"], "visibility": "in-collection"},
        )
        created["spaces"][item["key"]] = space["id"]
        _, section = api(
            "POST",
            f"/orgs/{ORG_ID}/sites/{SITE_ID}/sections",
            {"spaceId": space["id"], "title": item["title"], "icon": item["icon"], "draft": False},
        )
        section_id = section["id"]
        site_space_id = section["siteSpaces"][0]["id"]
        created["sections"][item["key"]] = section_id
        created["site_spaces"][item["key"]] = site_space_id
        api(
            "PATCH",
            f"/orgs/{ORG_ID}/sites/{SITE_ID}/sections/{section_id}",
            {"path": item["path"], "description": item["description"], "draft": False, "defaultSiteSpace": site_space_id},
        )
    api("PATCH", f"/orgs/{ORG_ID}/sites/{SITE_ID}", {"defaultSiteSection": created["sections"]["HOME"], "defaultSiteSpace": created["site_spaces"]["HOME"]})
    write("gitbook-created.json", json.dumps(created, indent=2))
    return created


def replace_sentinels(space_ids: dict[str, str]) -> None:
    replacements = {item["sentinel"]: space_ids[item["key"]] for item in SPACES}
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")


def import_spaces(created: dict) -> None:
    imports = {}
    for item in SPACES:
        status, _ = api(
            "POST",
            f"/spaces/{created['spaces'][item['key']]}/git/import",
            {
                "url": PUBLIC_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": item["folder"],
                "repoTreeURL": f"https://github.com/{PUBLIC_OWNER}/{PUBLIC_REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{PUBLIC_OWNER}/{PUBLIC_REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[item["key"]] = {"status": status, "space": created["spaces"][item["key"]], "folder": item["folder"]}
    write("gitbook-import-results.json", json.dumps(imports, indent=2))


def customize(created: dict) -> None:
    _, current = api("GET", f"/orgs/{ORG_ID}/sites/{SITE_ID}/customization")
    current["title"] = "NI Documentation Transformation Demo"
    current["localizedTitle"] = {}
    current["styling"] = {
        "theme": "clean",
        "primaryColor": {"light": "#F5C400", "dark": "#FFE36B"},
        "infoColor": {"light": "#235789", "dark": "#77B5E8"},
        "successColor": {"light": "#237A57", "dark": "#64D29C"},
        "warningColor": {"light": "#A16207", "dark": "#FACC15"},
        "dangerColor": {"light": "#B42318", "dark": "#F97066"},
        "tint": {"color": {"light": "#F8FAFC", "dark": "#111827"}},
        "corners": "straight",
        "depth": "flat",
        "links": "accent",
        "font": "Inter",
        "monospaceFont": "IBMPlexMono",
        "icons": "regular",
        "background": "plain",
        "sidebar": {"background": "filled", "list": "line"},
        "codeTheme": {"default": {"light": "default-light", "dark": "default-dark"}, "openapi": {"light": "default-light", "dark": "default-dark"}},
        "search": "prominent",
    }
    logo = f"{RAW}/assets/ni-wordmark.svg"
    current["favicon"] = {"icon": {"light": logo, "dark": logo}}
    current["header"] = {
        "logo": {"light": logo, "dark": logo},
        "primaryLink": {"kind": "space", "space": created["spaces"]["HOME"]},
        "links": [
            {"title": "Authoring", "style": "link", "to": {"kind": "space", "space": created["spaces"]["AUTHORING"]}, "links": []},
            {"title": "Localization", "style": "link", "to": {"kind": "space", "space": created["spaces"]["DELIVERY"]}, "links": []},
            {"title": "AI workflows", "style": "button-primary", "to": {"kind": "space", "space": created["spaces"]["AI"]}, "links": []},
            {"title": "Source repo", "style": "button-secondary", "to": {"kind": "url", "url": f"https://github.com/{PRIVATE_REPO}"}, "links": []},
        ],
    }
    current["footer"] = {
        "logo": {"light": logo, "dark": logo},
        "copyright": "First-draft GitBook demo for National Instruments.",
        "groups": [
            {
                "title": "Demo",
                "links": [
                    {"title": "Home", "to": {"kind": "space", "space": created["spaces"]["HOME"]}},
                    {"title": "Source repo", "to": {"kind": "url", "url": f"https://github.com/{PRIVATE_REPO}"}},
                ],
            }
        ],
    }
    current["ai"] = {
        "mode": "assistant",
        "suggestions": [
            "How does the TMS integration work?",
            "What is the recommended DITA to Markdown path?",
            "How can SMEs contribute through GitHub?",
            "Which metrics should NI track?",
        ],
    }
    current["pageActions"] = {"externalAI": True, "markdown": True, "mcp": True, "items": ["assistant", "markdown", "external-ai", "mcp", "pdf"]}
    current["feedback"] = {"enabled": True}
    current["pdf"] = {"enabled": True}
    current["pagination"] = {"enabled": True}
    current["git"] = {"showEditLink": True}
    current["themes"] = {"default": "system", "toggeable": True}
    api("PUT", f"/orgs/{ORG_ID}/sites/{SITE_ID}/customization", current)


def publish_and_share() -> dict:
    try:
        _, publish = api("POST", f"/orgs/{ORG_ID}/sites/{SITE_ID}/publish")
    except RuntimeError as exc:
        if "Site is already published" not in str(exc):
            raise
        _, publish = api("GET", f"/orgs/{ORG_ID}/sites/{SITE_ID}")
    _, share = api("POST", f"/orgs/{ORG_ID}/sites/{SITE_ID}/share-links", {"name": "NI demo review"})
    try:
        _, publish = api("POST", f"/orgs/{ORG_ID}/sites/{SITE_ID}/publish")
    except RuntimeError as exc:
        if "Site is already published" not in str(exc):
            raise
        _, publish = api("GET", f"/orgs/{ORG_ID}/sites/{SITE_ID}")
    final = {
        "site": SITE_ID,
        "app_url": publish["urls"]["app"],
        "preview_url": publish["urls"]["preview"],
        "published_url": share["urls"]["published"],
    }
    write("gitbook-publish-share.json", json.dumps(final, indent=2))
    return final


def main() -> None:
    scaffold_all()
    git_commit_push()
    push_public_mirror()
    created = create_gitbook_objects()
    replace_sentinels(created["spaces"])
    git_commit_push()
    push_public_mirror()
    import_spaces(created)
    customize(created)
    final = publish_and_share()
    git_commit_push()
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
