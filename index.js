// ==========================================================================
// ALPHAFOLDOLOGY HUB INTERACTIVE LOGIC (Vanilla JS)
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // App State
  let appData = {
    tools: [],
    socialPosts: [],
    metadata: {}
  };
  
  let currentFilters = {
    search: '',
    category: 'all',
    pub: 'all',
    sort: 'default'
  };
  
  let activeView = 'grid'; // 'grid' or 'table'
  let activeToolForEdit = null;
  
  // Lineage Tree Coordinates Configuration (computed dynamically at load time)
  let NODE_COORDINATES = {};
  let TREE_LINKS = [];
  let MAJOR_TOOL_IDS = new Set();

  // DOM Elements
  const statTotalTools = document.getElementById('stat-total-tools');
  const statTotalStars = document.getElementById('stat-total-stars');
  const statTotalCitations = document.getElementById('stat-total-citations');
  const statTotalPublished = document.getElementById('stat-total-published');
  const statTotalPreprints = document.getElementById('stat-total-preprints');
  const statLastUpdate = document.getElementById('stat-last-update');
  
  const searchInput = document.getElementById('search-input');
  const categoryChips = document.getElementById('category-chips');
  const pubChips = document.getElementById('pub-chips');
  const sortChips = document.getElementById('sort-chips');
  const resultsCount = document.getElementById('results-count');
  
  const toolsGrid = document.getElementById('tools-grid');
  const toolsTableContainer = document.getElementById('tools-table-container');
  const toolsTableBody = document.getElementById('tools-table-body');
  const tableViewWrapper = document.getElementById('table-view-wrapper');
  const floatingScrollbar = document.getElementById('floating-scrollbar');
  const floatingScrollbarInner = document.getElementById('floating-scrollbar-inner');
  const toolsTable = document.getElementById('tools-table');
  
  const btnViewGrid = document.getElementById('btn-view-grid');
  const btnViewTable = document.getElementById('btn-view-table');
  
  const socialFeed = document.getElementById('social-feed');
  
  // Modal Elements
  const detailModal = document.getElementById('detail-modal');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const modalCategory = document.getElementById('modal-category');
  const modalDate = document.getElementById('modal-date');
  const modalTitle = document.getElementById('modal-title');
  const modalStatus = document.getElementById('modal-status');
  const modalDescription = document.getElementById('modal-description');
  const modalStrengths = document.getElementById('modal-strengths');
  const modalWeaknesses = document.getElementById('modal-weaknesses');
  const modalUsage = document.getElementById('modal-usage');
  const modalStars = document.getElementById('modal-stars');
  const modalForks = document.getElementById('modal-forks');
  const modalIssues = document.getElementById('modal-issues');
  const modalCitations = document.getElementById('modal-citations');
  const modalGithubLink = document.getElementById('modal-github-link');
  const modalHfLink = document.getElementById('modal-hf-link');
  const modalParent = document.getElementById('modal-parent');
  const modalForksList = document.getElementById('modal-forks-list');
  const modalPapersList = document.getElementById('modal-papers-list');
  
  // Suggest Correction Elements
  const modalDetailBody = document.getElementById('modal-detail-body');
  const modalDerivativesSection = document.getElementById('modal-derivatives-section');
  const modalSuggestEditBtn = document.getElementById('modal-suggest-edit-btn');
  const modalEditPanel = document.getElementById('modal-edit-panel');
  const btnEditBack = document.getElementById('btn-edit-back');
  const editFieldSelect = document.getElementById('edit-field-select');
  const editCurrentValue = document.getElementById('edit-current-value');
  const editProposedValue = document.getElementById('edit-proposed-value');
  const editEvidence = document.getElementById('edit-evidence');
  const editPatchPreview = document.getElementById('edit-patch-preview');
  const btnSubmitGithubIssue = document.getElementById('btn-submit-github-issue');
  const btnCopyEditJson = document.getElementById('btn-copy-edit-json');
  const editPanelToolName = document.getElementById('edit-panel-tool-name');

  // Zoom State for Tree
  let zoomScale = 1.0;
  let panX = 0;
  let panY = 0;
  const svgTree = document.getElementById('svg-tree');
  const viewportGroup = document.getElementById('viewport-group');
  const treeCanvas = document.getElementById('tree-canvas');
  let isDragging = false;
  let startX, startY;

  // Initialize Application
  fetch('tools_data.json?v=17')
    .then(response => {
      if (!response.ok) throw new Error('Data file not found');
      return response.json();
    })
    .then(data => {
      appData = data;
      // Select major tools by academic citations and GitHub stars to keep starting view clean and readable
      const curatedTools = appData.tools.slice(0, 101);
      const toolsByCategory = {};
      curatedTools.forEach(tool => {
        if (!toolsByCategory[tool.category]) {
          toolsByCategory[tool.category] = [];
        }
        toolsByCategory[tool.category].push(tool);
      });

      MAJOR_TOOL_IDS = new Set();

      // For each category, sort by importance = stars + citations, and take top 5
      Object.keys(toolsByCategory).forEach(cat => {
        const sorted = [...toolsByCategory[cat]].sort((a, b) => {
          const scoreA = (a.github_stars || 0) + (a.citations_count || 0);
          const scoreB = (b.github_stars || 0) + (b.citations_count || 0);
          return scoreB - scoreA;
        });
        const top5 = sorted.slice(0, 5);
        top5.forEach(t => MAJOR_TOOL_IDS.add(t.id));
      });

      // Always include base progenitors
      ['alphafold1', 'alphafold2', 'rosettafold'].forEach(id => {
        if (appData.tools.some(t => t.id === id)) {
          MAJOR_TOOL_IDS.add(id);
        }
      });

      // Recursively trace parents to maintain connected lineage paths
      let addedAny = true;
      while (addedAny) {
        addedAny = false;
        const currentIds = Array.from(MAJOR_TOOL_IDS);
        for (let i = 0; i < currentIds.length; i++) {
          const id = currentIds[i];
          const tool = appData.tools.find(t => t.id === id);
          if (tool && tool.parent && !MAJOR_TOOL_IDS.has(tool.parent)) {
            MAJOR_TOOL_IDS.add(tool.parent);
            addedAny = true;
          }
        }
      }

      computeDynamicLayout();
      populateMetrics();
      renderSocialFeed();
      drawLineageTree();
      filterAndRenderContent();
      setTimeout(fitViewToMajorNodes, 100);
    })
    .catch(error => {
      console.error("Failed to load Alphafoldology dataset:", error);
      alert("Could not load tool database. Run the scraper script first or check your file path.");
    });

  // Calculate dynamic X/Y timeline coordinates and stagger vertical lanes to avoid collision
  function computeDynamicLayout() {
    NODE_COORDINATES = {};
    TREE_LINKS = [];

    // Parse and determine min/max dates dynamically
    let minTime = Infinity;
    let maxTime = -Infinity;
    
    appData.tools.forEach(tool => {
      if (tool.date) {
        const t = new Date(tool.date).getTime();
        if (t < minTime) minTime = t;
        if (t > maxTime) maxTime = t;
      }
    });

    // Fallback bounds if no dates or invalid data
    const minDate = (minTime !== Infinity) ? minTime : new Date('2018-01-01').getTime();
    const maxDate = (maxTime !== -Infinity) ? maxTime : new Date('2026-12-31').getTime();

    const minX = 150;
    const maxX = 4350;

    const CATEGORY_LANES = {
      'Core Predictors': 0,
      'Fast Predictors': 1,
      'Databases': 2,
      'Visualization': 3,
      'Structural Search': 4,
      'Variant Predictors': 5,
      'Ligand Docking': 6,
      'Protein Docking': 7,
      'Protein Design': 8,
      'Ensemble Generators': 9,
      'Benchmarks': 10,
      'Scoring': 11,
      'Training': 12
    };

    // Staggering slots (5 slots per category lane)
    const lastPlacedX = {};
    Object.keys(CATEGORY_LANES).forEach(cat => {
      lastPlacedX[cat] = Array(5).fill(-Infinity);
    });

    // Sort tools chronologically to layout nodes from left to right
    const sortedTools = [...appData.tools].sort((a, b) => {
      const dateA = a.date ? new Date(a.date).getTime() : 0;
      const dateB = b.date ? new Date(b.date).getTime() : 0;
      return dateA - dateB;
    });

    sortedTools.forEach(tool => {
      const cat = tool.category;
      const laneIndex = CATEGORY_LANES[cat] !== undefined ? CATEGORY_LANES[cat] : 4; // default center lane
      
      // Calculate X coordinate using piecewise mapping to compress empty early space before AlphaFold 2
      const dateVal = tool.date ? new Date(tool.date).getTime() : minDate;
      const clampedVal = Math.max(minDate, Math.min(maxDate, dateVal));
      const pivotX = 500;
      const pivotDate = new Date('2021-07-15').getTime();
      let x;
      if (clampedVal <= pivotDate) {
        const range = pivotDate - minDate || 1;
        const pct = (clampedVal - minDate) / range;
        x = minX + pct * (pivotX - minX);
      } else {
        const range = maxDate - pivotDate || 1;
        const pct = (clampedVal - pivotDate) / range;
        x = pivotX + pct * (maxX - pivotX);
      }

      // Find available slot (0-4) using greedy spacing
      if (!lastPlacedX[cat]) {
        lastPlacedX[cat] = Array(5).fill(-Infinity);
      }
      const slots = lastPlacedX[cat];
      let chosenSlot = 0;
      let minLastX = Infinity;
      let found = false;

      for (let s = 0; s < 5; s++) {
        if (x - slots[s] >= 120) {
          chosenSlot = s;
          found = true;
          break;
        }
        if (slots[s] < minLastX) {
          minLastX = slots[s];
          chosenSlot = s;
        }
      }

      slots[chosenSlot] = x;

      // Calculate Y coordinate with staggered offsets
      const laneY = 150 + laneIndex * 262.5;
      const offsets = [-75, -35, 0, 35, 75];
      const y = laneY + offsets[chosenSlot];

      // Map to CSS node types
      let nodeType = 'other';
      if (cat === 'Core Predictors') nodeType = 'core';
      else if (cat === 'Fast Predictors') nodeType = 'fast';
      else if (cat === 'Protein Design') nodeType = 'design';
      else if (cat === 'Variant Predictors') nodeType = 'variant';
      else if (cat === 'Structural Search') nodeType = 'search';
      else if (cat === 'Ligand Docking') nodeType = 'ligand-docking';
      else if (cat === 'Protein Docking') nodeType = 'protein-docking';
      else if (cat === 'Databases') nodeType = 'databases';
      else if (cat === 'Visualization') nodeType = 'visualization';
      else if (cat === 'Ensemble Generators') nodeType = 'ensemble';
      else if (cat === 'Benchmarks') nodeType = 'benchmarks';
      else if (cat === 'Scoring') nodeType = 'scoring';

      NODE_COORDINATES[tool.id] = {
        x: x,
        y: y,
        type: nodeType,
        label: tool.name
      };
    });

    // Populate TREE_LINKS dynamically based on parents that are actually present
    appData.tools.forEach(tool => {
      if (tool.parent && NODE_COORDINATES[tool.parent]) {
        TREE_LINKS.push({
          source: tool.parent,
          target: tool.id
        });
      }
    });
  }

  // Populate Metrics Header
  function populateMetrics() {
    statTotalTools.textContent = appData.metadata.total_tools || 0;
    statTotalStars.textContent = formatNum(appData.metadata.total_github_stars || 0);
    statTotalCitations.textContent = formatNum(appData.metadata.total_citations || 0);
    
    // Compute or retrieve preprint/published counts
    let publishedCount = appData.metadata.total_published_papers;
    let preprintsCount = appData.metadata.total_preprints;
    if (publishedCount === undefined || preprintsCount === undefined) {
      publishedCount = 0;
      preprintsCount = 0;
      appData.tools.forEach(tool => {
        if (tool.publication_type === 'published') {
          publishedCount++;
        } else if (tool.publication_type === 'preprint') {
          preprintsCount++;
        }
      });
    }
    statTotalPublished.textContent = formatNum(publishedCount);
    statTotalPreprints.textContent = formatNum(preprintsCount);
    
    // Format timestamp nicely
    const dateStr = appData.metadata.last_updated || 'Unknown';
    statLastUpdate.textContent = dateStr.split(' ')[0]; // YYYY-MM-DD
  }

  function formatNum(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
    return num;
  }

  // Render Social Feed
  function renderSocialFeed() {
    socialFeed.innerHTML = '';
    const posts = appData.social_posts || [];
    
    posts.forEach(post => {
      const date = new Date(post.created_at).toLocaleDateString(undefined, {month: 'short', day: 'numeric'});
      const avatarChar = post.author_name.charAt(0).toUpperCase();
      
      const postEl = document.createElement('div');
      postEl.className = 'social-post';
      postEl.innerHTML = `
        <div class="post-author">
          <div class="author-avatar">${avatarChar}</div>
          <div class="author-info">
            <span class="author-name">${post.author_name}</span>
            <span class="author-handle">@${post.author_handle}</span>
          </div>
        </div>
        <p class="post-text">${post.text}</p>
        <div class="post-footer">
          <span>❤️ ${post.likes}</span>
          <span>🔄 ${post.reposts}</span>
          <span>📅 ${date}</span>
          <a href="${post.uri}" target="_blank" style="margin-left:auto; color:var(--accent-cyan); text-decoration:none;">View</a>
        </div>
      `;
      socialFeed.appendChild(postEl);
    });
  }

  // Render S-curve connections & node groups in SVG
  function drawLineageTree() {
    const svgConnections = document.getElementById('svg-connections');
    const svgNodes = document.getElementById('svg-nodes');
    
    svgConnections.innerHTML = '';
    svgNodes.innerHTML = '';

    // 1. Draw connections (Cubic Bezier S-Curves)
    TREE_LINKS.forEach(link => {
      const src = NODE_COORDINATES[link.source];
      const tgt = NODE_COORDINATES[link.target];
      if (!src || !tgt) return;

      const isMinorLink = !MAJOR_TOOL_IDS.has(link.source) || !MAJOR_TOOL_IDS.has(link.target);

      const pathData = drawBezier(src.x, src.y, tgt.x, tgt.y);
      const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
      pathEl.setAttribute("d", pathData);
      pathEl.setAttribute("class", `tree-link ${isMinorLink ? 'link-minor' : 'link-major'}`);
      pathEl.setAttribute("id", `link-${link.source}-${link.target}`);
      pathEl.setAttribute("stroke", "var(--bg-tertiary)");
      svgConnections.appendChild(pathEl);
    });

    // 2. Draw nodes
    Object.keys(NODE_COORDINATES).forEach(key => {
      const node = NODE_COORDINATES[key];
      const toolInfo = appData.tools.find(t => t.id === key) || {};
      const isMinor = !MAJOR_TOOL_IDS.has(key);
      
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", `tree-node node-${node.type} ${toolInfo.status === 'Active' ? 'node-active' : ''} ${isMinor ? 'node-minor' : 'node-major'}`);
      g.setAttribute("id", `node-${key}`);
      g.setAttribute("transform", `translate(${node.x}, ${node.y})`);
      
      // Node circle - larger for major tools
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("r", isMinor ? "22" : "36");
      g.appendChild(circle);
      
      // Node Label (First Line: Acronym)
      const text1 = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text1.setAttribute("y", isMinor ? "1" : "0");
      text1.textContent = node.label;
      g.appendChild(text1);

      // Sub-label (Category type label)
      const text2 = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text2.setAttribute("y", isMinor ? "12" : "15");
      text2.setAttribute("class", "node-type");
      text2.textContent = node.type.toUpperCase();
      g.appendChild(text2);

      // Interactions
      g.addEventListener('click', () => {
        openModal(key);
      });

      g.addEventListener('mouseenter', () => {
        highlightNodeConnections(key, true);
      });

      g.addEventListener('mouseleave', () => {
        highlightNodeConnections(key, false);
      });

      svgNodes.appendChild(g);
    });
  }

  // Draw Bezier S-Curve path
  function drawBezier(x1, y1, x2, y2) {
    const cp1x = x1 + (x2 - x1) * 0.45;
    const cp1y = y1;
    const cp2x = x1 + (x2 - x1) * 0.55;
    const cp2y = y2;
    return `M ${x1} ${y1} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${x2} ${y2}`;
  }

  // Highlight connections associated with a node
  function highlightNodeConnections(nodeId, highlight) {
    TREE_LINKS.forEach(link => {
      if (link.source === nodeId || link.target === nodeId) {
        const linkEl = document.getElementById(`link-${link.source}-${link.target}`);
        if (linkEl) {
          if (highlight) {
            linkEl.classList.add('highlight');
            linkEl.setAttribute("stroke", "var(--accent-cyan)");
          } else {
            linkEl.classList.remove('highlight');
            linkEl.setAttribute("stroke", "var(--bg-tertiary)");
          }
        }
      }
    });
  }

  // Filter and dynamic content rendering
  function filterAndRenderContent() {
    const query = currentFilters.search.toLowerCase().trim();
    const cat = currentFilters.category;
    const pub = currentFilters.pub;

    // Filter tools
    const filteredTools = appData.tools.filter(tool => {
      const matchSearch = 
        tool.name.toLowerCase().includes(query) ||
        tool.usage.toLowerCase().includes(query) ||
        tool.strengths.toLowerCase().includes(query) ||
        tool.weaknesses.toLowerCase().includes(query) ||
        tool.category.toLowerCase().includes(query);

      const matchCat = (cat === 'all' || tool.category === cat);
      
      const matchPub = (pub === 'all' || 
                        (pub === 'published' && (tool.publication_type === 'published' || tool.paper_doi)) || 
                        (pub === 'preprint' && (tool.publication_type === 'preprint' || tool.preprint_doi)));

      return matchSearch && matchCat && matchPub;
    });

    // Sort filtered tools
    const sortVal = currentFilters.sort;
    if (sortVal === 'date-desc') {
      filteredTools.sort((a, b) => {
        const da = a.date ? new Date(a.date).getTime() : 0;
        const db = b.date ? new Date(b.date).getTime() : 0;
        return db - da; // newest first
      });
    } else if (sortVal === 'stars-desc') {
      filteredTools.sort((a, b) => {
        const sa = a.github_stars || 0;
        const sb = b.github_stars || 0;
        return sb - sa; // highest stars first
      });
    } else if (sortVal === 'citations-desc') {
      filteredTools.sort((a, b) => {
        const ca = a.citations_count || 0;
        const cb = b.citations_count || 0;
        return cb - ca; // highest citations first
      });
    } else {
      // Default: Restore original database order (topological genealogy sequence)
      const originalIndex = {};
      appData.tools.forEach((t, idx) => {
        originalIndex[t.id] = idx;
      });
      filteredTools.sort((a, b) => originalIndex[a.id] - originalIndex[b.id]);
    }

    resultsCount.textContent = `Showing ${filteredTools.length} tool${filteredTools.length === 1 ? '' : 's'}`;

    // Render Grid view
    renderGrid(filteredTools);

    // Render Table view
    renderTable(filteredTools);

    // Update Lineage Tree Node Opacities
    Object.keys(NODE_COORDINATES).forEach(key => {
      const nodeEl = document.getElementById(`node-${key}`);
      if (nodeEl) {
        const isMatched = filteredTools.some(t => t.id === key);
        if (query === '' && cat === 'all') {
          nodeEl.style.opacity = '1';
        } else {
          nodeEl.style.opacity = isMatched ? '1' : '0.15';
        }
      }
    });
  }

  // Render Grid Layout
  function renderGrid(toolsList) {
    toolsGrid.innerHTML = '';
    
    if (toolsList.length === 0) {
      toolsGrid.innerHTML = `
        <div style="grid-column: 1/-1; padding: 3rem; text-align: center; color: var(--text-muted); background: var(--card-bg); border: 1px dashed var(--card-border); border-radius: 16px;">
          <h3>No tools match your filter criteria.</h3>
          <p style="margin-top: 0.5rem; font-size: 0.9rem;">Try clearing your search query or selecting "All" categories.</p>
        </div>
      `;
      return;
    }

    toolsList.forEach(tool => {
      const catClass = getCategoryClass(tool.category);
      
      const card = document.createElement('div');
      card.className = `tool-card ${catClass}`;
      card.innerHTML = `
        <div class="card-top">
          <div class="card-meta cat-${catClass}">
            <span class="card-cat-badge">${tool.category}</span>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <span class="card-date-badge">${tool.date || '—'}</span>
              ${tool.publication_type && tool.publication_type !== 'unknown' ? `<span class="pub-type-badge pub-type-${tool.publication_type}">${tool.publication_type === 'published' ? '📄 Published' : '📝 Preprint'}</span>` : ''}
              <span class="status-indicator ${tool.status.toLowerCase()}">
                <span class="status-dot"></span>
                ${tool.status}
              </span>
            </div>
          </div>
          <div class="tool-name-container">
            <h3 class="tool-title-click" data-id="${tool.id}" style="cursor: pointer; display: inline-block;" title="Click to view details">${tool.name}${tool.hf_repo ? ' <span title="Available on HuggingFace" style="font-size: 0.9em; cursor: help;">🤗</span>' : ''}</h3>
            <p class="tool-desc">${tool.github_description || tool.usage}</p>
          </div>
        </div>

        <div>
          <div class="card-metrics">
            <div class="card-stat">
              <span>GitHub Stars</span>
              <strong>${tool.github_stars ? formatNum(tool.github_stars) : '—'}</strong>
            </div>
            <div class="card-stat">
              <span>Citations</span>
              <strong>${tool.citations_count ? formatNum(tool.citations_count) : '—'}</strong>
            </div>
          </div>

          <div class="card-sw-summary">
            <div class="sw-item pro">
              <span class="sw-bullet">✓</span>
              <span class="sw-text" title="${tool.strengths}">${tool.strengths}</span>
            </div>
            <div class="sw-item con">
              <span class="sw-bullet">✗</span>
              <span class="sw-text" title="${tool.weaknesses}">${tool.weaknesses}</span>
            </div>
          </div>

          <div class="card-pub-buttons" style="margin-bottom: 1.25rem; display: flex; flex-direction: column; gap: 0.5rem;">
            ${tool.paper_doi ? (() => {
              let paperShort = tool.short_citation;
              if (!paperShort) {
                const year = tool.date ? new Date(tool.date).getFullYear() : 'Unknown';
                paperShort = `Journal, ${year}`;
              }
              return `<a href="https://doi.org/${tool.paper_doi}" target="_blank" class="btn-pub btn-pub-paper" title="View Journal Publication (DOI: ${tool.paper_doi})">
                <span class="pub-icon">📄</span>
                <span class="pub-text" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${paperShort}</span>
              </a>`;
            })() : ''}
            ${tool.preprint_doi ? (() => {
              let preprintShort = tool.preprint_short_citation;
              if (!preprintShort) {
                const year = tool.date ? new Date(tool.date).getFullYear() : 'Unknown';
                preprintShort = `Preprint, ${year}`;
              }
              return `<a href="https://doi.org/${tool.preprint_doi}" target="_blank" class="btn-pub btn-pub-preprint" title="View Preprint (DOI: ${tool.preprint_doi})">
                <span class="pub-icon">📝</span>
                <span class="pub-text" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${preprintShort}</span>
              </a>`;
            })() : ''}
            ${(!tool.paper_doi && !tool.preprint_doi) ? `
              <div class="btn-pub btn-pub-none" style="opacity: 0.5; cursor: not-allowed;">
                <span class="pub-icon">🚫</span>
                <span class="pub-text">No Publication Listed</span>
              </div>
            ` : ''}
          </div>

          <div class="card-actions">
            <button class="btn btn-secondary btn-details" data-id="${tool.id}">Explore Derivatives</button>
            ${tool.repo ? `<a href="https://github.com/${tool.repo}" target="_blank" class="btn btn-primary">Repo</a>` : `<span class="btn btn-secondary" style="opacity: 0.5; cursor: not-allowed;" title="No public repository available">No Repo</span>`}
          </div>
        </div>
      `;
      
      // Bind click on Tool Name
      card.querySelector('.tool-title-click').addEventListener('click', () => {
        openModal(tool.id);
      });
      
      // Bind click on "Explore Derivatives"
      card.querySelector('.btn-details').addEventListener('click', () => {
        openModal(tool.id);
      });

      toolsGrid.appendChild(card);
    });
  }

  // Render Table Layout
  function renderTable(toolsList) {
    toolsTableBody.innerHTML = '';
    
    if (toolsList.length === 0) {
      toolsTableBody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 3rem; color: var(--text-muted);">
            No tools match filter criteria.
          </td>
        </tr>
      `;
      return;
    }

    toolsList.forEach(tool => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td class="tool-title-click" data-id="${tool.id}" style="cursor: pointer;" title="Click to view details"><strong>${tool.name}</strong>${tool.hf_repo ? ' <span title="Available on HuggingFace" style="font-size: 0.9em; cursor: help;">🤗</span>' : ''}</td>
        <td><span class="card-cat-badge">${tool.category}</span></td>
        <td><span class="status-badge ${tool.status.toLowerCase()}">${tool.status}</span></td>
        <td><span class="table-date">${tool.date || '—'}</span></td>
        <td>${tool.github_stars ? tool.github_stars.toLocaleString() : '—'}</td>
        <td>
          ${tool.citations_count ? tool.citations_count.toLocaleString() : '—'}
          ${tool.paper_doi ? `<a href="https://doi.org/${tool.paper_doi}" target="_blank" title="View Journal Publication (DOI: ${tool.paper_doi})" style="color: var(--accent-cyan); text-decoration: none; margin-left: 0.5rem; font-size: 0.82rem; display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 4px; background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.2);">📄</a>` : ''}
          ${tool.preprint_doi ? `<a href="https://doi.org/${tool.preprint_doi}" target="_blank" title="View Preprint (DOI: ${tool.preprint_doi})" style="color: #ec4899; text-decoration: none; margin-left: 0.35rem; font-size: 0.82rem; display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 4px; background: rgba(236, 72, 153, 0.1); border: 1px solid rgba(236, 72, 153, 0.2);">✍️</a>` : ''}
        </td>
        <td>
          <button class="btn btn-secondary btn-details-table" data-id="${tool.id}" style="padding: 0.35rem 0.75rem; font-size: 0.78rem;">Details</button>
        </td>
      `;
      
      // Bind click on Name Cell
      row.querySelector('.tool-title-click').addEventListener('click', () => {
        openModal(tool.id);
      });
      
      row.querySelector('.btn-details-table').addEventListener('click', () => {
        openModal(tool.id);
      });
      
      toolsTableBody.appendChild(row);
    });
    
    // Update scrollbar width after table render
    if (activeView === 'table') {
      setTimeout(updateFloatingScrollbar, 50);
    }
  }

  function getCategoryClass(category) {
    switch (category) {
      case 'Core Predictors': return 'cat-core';
      case 'Fast Predictors': return 'cat-fast';
      case 'Protein Design': return 'cat-design';
      case 'Variant Predictors': return 'cat-variant';
      case 'Structural Search': return 'cat-search';
      case 'Ligand Docking': return 'cat-ligand-docking';
      case 'Protein Docking': return 'cat-protein-docking';
      case 'Databases': return 'cat-databases';
      case 'Visualization': return 'cat-visualization';
      case 'Ensemble Generators': return 'cat-ensemble';
      case 'Benchmarks': return 'cat-benchmarks';
      case 'Scoring': return 'cat-scoring';
      case 'Training': return 'cat-training';
      default: return 'cat-other';
    }
  }

  // Detail Modal Manager
  function openModal(id) {
    const tool = appData.tools.find(t => t.id === id);
    if (!tool) return;

    activeToolForEdit = tool;
    resetEditPanel();

    modalCategory.textContent = tool.category;
    modalCategory.className = `chip cat-${getCategoryClass(tool.category)}`;
    modalDate.textContent = tool.date || '—';
    modalTitle.textContent = tool.name;
    modalStatus.textContent = tool.status;
    modalStatus.className = `status-badge ${tool.status.toLowerCase()}`;
    
    // Publication type badge in modal
    let pubBadgeEl = document.getElementById('modal-pub-type-badge');
    if (!pubBadgeEl) {
      pubBadgeEl = document.createElement('span');
      pubBadgeEl.id = 'modal-pub-type-badge';
      modalStatus.parentNode.insertBefore(pubBadgeEl, modalStatus.nextSibling);
    }
    if (tool.publication_type && tool.publication_type !== 'unknown') {
      pubBadgeEl.className = `pub-type-badge pub-type-${tool.publication_type}`;
      pubBadgeEl.textContent = tool.publication_type === 'published' ? '📄 Published' : '📝 Preprint';
      pubBadgeEl.style.display = 'inline-block';
      pubBadgeEl.style.marginLeft = '0.5rem';
    } else {
      pubBadgeEl.style.display = 'none';
    }
    
    modalDescription.textContent = tool.github_description || tool.usage;
    modalStrengths.textContent = tool.strengths;
    modalWeaknesses.textContent = tool.weaknesses;
    modalUsage.textContent = tool.usage;
    
    // Populate Full Citation below weaknesses
    const modalCitationSection = document.getElementById('modal-citation-section');
    const modalFullCitation = document.getElementById('modal-full-citation');
    if (modalCitationSection && modalFullCitation) {
      let citationsHtml = [];
      if (tool.full_citation) {
        let citation = tool.full_citation;
        if (tool.paper_doi) {
          citation += ` doi: <a href="https://doi.org/${tool.paper_doi}" target="_blank" style="color: var(--accent-cyan); text-decoration: none; border-bottom: 1px dashed var(--accent-cyan);">${tool.paper_doi}</a>`;
        }
        citationsHtml.push(`<div><strong>Journal Paper:</strong> ${citation}</div>`);
      }
      if (tool.preprint_full_citation) {
        let citation = tool.preprint_full_citation;
        if (tool.preprint_doi) {
          citation += ` doi: <a href="https://doi.org/${tool.preprint_doi}" target="_blank" style="color: var(--accent-cyan); text-decoration: none; border-bottom: 1px dashed var(--accent-cyan);">${tool.preprint_doi}</a>`;
        }
        citationsHtml.push(`<div><strong>Preprint:</strong> ${citation}</div>`);
      }
      
      if (citationsHtml.length > 0) {
        modalFullCitation.innerHTML = citationsHtml.join('<div style="margin-top:0.5rem;"></div>');
        modalCitationSection.style.display = 'block';
      } else {
        modalCitationSection.style.display = 'none';
      }
    }
    
    modalStars.textContent = tool.github_stars ? tool.github_stars.toLocaleString() : '—';
    modalForks.textContent = tool.github_forks ? tool.github_forks.toLocaleString() : '—';
    modalIssues.textContent = tool.github_open_issues ? tool.github_open_issues.toLocaleString() : '—';
    modalCitations.textContent = tool.citations_count ? tool.citations_count.toLocaleString() : '—';
    
    if (tool.repo) {
      modalGithubLink.href = `https://github.com/${tool.repo}`;
      modalGithubLink.style.display = 'block';
    } else {
      modalGithubLink.href = '#';
      modalGithubLink.style.display = 'none';
    }

    if (tool.hf_repo) {
      modalHfLink.href = `https://huggingface.co/${tool.hf_repo}`;
      modalHfLink.style.display = 'block';
    } else {
      modalHfLink.href = '#';
      modalHfLink.style.display = 'none';
    }

    const modalPaperDoiLink = document.getElementById('modal-paper-doi-link');
    const modalPaperDoiContainer = document.getElementById('modal-paper-doi-container');
    if (tool.paper_doi) {
      modalPaperDoiLink.href = `https://doi.org/${tool.paper_doi}`;
      modalPaperDoiLink.textContent = tool.paper_doi;
      modalPaperDoiLink.title = `doi: ${tool.paper_doi}`;
      modalPaperDoiContainer.style.display = 'flex';
    } else {
      modalPaperDoiContainer.style.display = 'none';
    }

    const modalPreprintDoiLink = document.getElementById('modal-preprint-doi-link');
    const modalPreprintDoiContainer = document.getElementById('modal-preprint-doi-container');
    if (tool.preprint_doi) {
      modalPreprintDoiLink.href = `https://doi.org/${tool.preprint_doi}`;
      modalPreprintDoiLink.textContent = tool.preprint_doi;
      modalPreprintDoiLink.title = `preprint doi: ${tool.preprint_doi}`;
      modalPreprintDoiContainer.style.display = 'flex';
    } else {
      modalPreprintDoiContainer.style.display = 'none';
    }
    
    // Parent connection
    if (tool.parent) {
      const parentTool = appData.tools.find(t => t.id === tool.parent);
      modalParent.innerHTML = `<span style="color:var(--accent-cyan); cursor:pointer;" id="modal-parent-link">${parentTool ? parentTool.name : tool.parent}</span>`;
      document.getElementById('modal-parent-link').addEventListener('click', () => {
        openModal(tool.parent);
      });
    } else {
      modalParent.textContent = 'None (Primary Progenitor)';
    }

    // Populate forks
    modalForksList.innerHTML = '';
    const forks = tool.github_top_forks || [];
    if (forks.length === 0) {
      modalForksList.innerHTML = `<li><div class="derivative-desc">No active public forks harvested.</div></li>`;
    } else {
      forks.forEach(fork => {
        const li = document.createElement('li');
        li.innerHTML = `
          <a href="${fork.url}" target="_blank">${fork.name}</a>
          <span class="derivative-desc">${fork.description || 'No description provided.'}</span>
          <span class="derivative-meta">⭐ ${fork.stars} stars</span>
        `;
        modalForksList.appendChild(li);
      });
    }

    // Populate citations
    modalPapersList.innerHTML = '';
    const papers = tool.citing_papers || [];
    if (papers.length === 0) {
      modalPapersList.innerHTML = `<li><div class="derivative-desc">No highly cited derivative papers fetched.</div></li>`;
    } else {
      papers.forEach(paper => {
        const li = document.createElement('li');
        let titleHtml = `<span class="derivative-title" style="font-weight: 500; color: var(--text-main); display: block; margin-bottom: 0.15rem;">${paper.title}</span>`;
        let linkHtml = '';
        if (paper.url) {
          if (paper.url.startsWith('https://doi.org/')) {
            const doiVal = paper.url.substring('https://doi.org/'.length);
            linkHtml = ` doi: <a href="${paper.url}" target="_blank" style="color: var(--accent-cyan); text-decoration: none; border-bottom: 1px dashed var(--accent-cyan);">${doiVal}</a>`;
          } else {
            linkHtml = ` link: <a href="${paper.url}" target="_blank" style="color: var(--accent-cyan); text-decoration: none; border-bottom: 1px dashed var(--accent-cyan);">link</a>`;
          }
        }
        li.innerHTML = `
          ${titleHtml}
          <span class="derivative-desc" style="display: block; font-size: 0.82rem; color: var(--text-muted); margin-bottom: 0.15rem;">by ${paper.authors} (${paper.year})${linkHtml}</span>
          <span class="derivative-meta" style="display: block; font-size: 0.78rem; color: var(--accent-cyan); font-weight: 500;">🔥 Cited by ${paper.citations} times</span>
        `;
        modalPapersList.appendChild(li);
      });
    }

    // Activate modal
    detailModal.classList.add('active');
  }

  function closeModal() {
    detailModal.classList.remove('active');
    resetEditPanel();
  }

  modalCloseBtn.addEventListener('click', closeModal);
  detailModal.addEventListener('click', (e) => {
    if (e.target === detailModal) closeModal();
  });

  // ==========================================================================
  // Suggest Correction & Data Issue Flagging Logic
  // ==========================================================================
  function resetEditPanel() {
    if (modalDetailBody && modalDerivativesSection && modalEditPanel) {
      modalDetailBody.style.display = '';
      modalDerivativesSection.style.display = '';
      modalEditPanel.style.display = 'none';
    }
  }

  if (modalSuggestEditBtn) {
    modalSuggestEditBtn.addEventListener('click', () => {
      if (!activeToolForEdit) return;
      
      // Toggle visibility
      modalDetailBody.style.display = 'none';
      modalDerivativesSection.style.display = 'none';
      modalEditPanel.style.display = 'flex';
      
      // Set panel title
      editPanelToolName.textContent = activeToolForEdit.name;
      
      // Reset form controls
      editFieldSelect.value = 'paper_doi';
      populateCurrentValue();
      editProposedValue.placeholder = 'Enter corrected value here...';
      editProposedValue.disabled = false;
      editProposedValue.style.backgroundColor = '';
      editProposedValue.value = '';
      editEvidence.value = '';
      updatePatchPreview();
    });
  }

  if (btnEditBack) {
    btnEditBack.addEventListener('click', resetEditPanel);
  }

  function populateCurrentValue() {
    if (!activeToolForEdit) return;
    const field = editFieldSelect.value;
    if (field === 'remove') {
      editCurrentValue.value = 'Entire tool entry';
      updatePatchPreview();
      return;
    }
    let val = activeToolForEdit[field];
    if (val === undefined || val === null) {
      val = '—';
    } else if (typeof val === 'object') {
      val = JSON.stringify(val);
    }
    editCurrentValue.value = val;
    updatePatchPreview();
  }

  if (editFieldSelect) {
    editFieldSelect.addEventListener('change', () => {
      populateCurrentValue();
      const field = editFieldSelect.value;
      if (field === 'remove') {
        editProposedValue.value = '';
        editProposedValue.placeholder = 'N/A (Reason for removal goes in Sources below)';
        editProposedValue.disabled = true;
        editProposedValue.style.backgroundColor = 'rgba(15,23,42,0.04)';
      } else {
        editProposedValue.placeholder = 'Enter corrected value here...';
        editProposedValue.disabled = false;
        editProposedValue.style.backgroundColor = '';
        editProposedValue.value = '';
      }
      updatePatchPreview();
    });
  }

  if (editProposedValue) {
    editProposedValue.addEventListener('input', updatePatchPreview);
  }
  if (editEvidence) {
    editEvidence.addEventListener('input', updatePatchPreview);
  }

  function generateProposalMarkdown() {
    if (!activeToolForEdit) return '';
    const field = editFieldSelect.value;
    const fieldLabel = editFieldSelect.options[editFieldSelect.selectedIndex].text;
    const evidence = editEvidence.value.trim();

    if (field === 'remove') {
      return `### Tool/Method Removal Request

- **Tool/Method Name:** ${activeToolForEdit.name} (ID: \`${activeToolForEdit.id}\`)
- **Action:** Requesting removal of this entire tool entry from the database.
- **GitHub Repository:** ${activeToolForEdit.repo ? `https://github.com/${activeToolForEdit.repo}` : 'N/A'}
- **Reason for Removal / Evidence:** ${evidence ? evidence : 'None specified.'}

---
Proposed action: Delete the JSON object for \`${activeToolForEdit.id}\` from \`tools_data.json\`.`;
    }

    const currentVal = activeToolForEdit[field] !== undefined ? activeToolForEdit[field] : null;
    const proposedVal = editProposedValue.value.trim();

    return `### Tool Data Correction Proposal

- **Tool:** ${activeToolForEdit.name} (ID: \`${activeToolForEdit.id}\`)
- **Field to Correct:** \`${fieldLabel}\` (\`${field}\`)
- **Current Value:** \`${currentVal !== null ? currentVal : 'None'}\`
- **Proposed Value:** \`${proposedVal ? proposedVal : 'None'}\`
- **Evidence / Verification:** ${evidence ? evidence : 'None specified.'}

---
#### Proposed JSON Patch:
\`\`\`json
{
  "id": "${activeToolForEdit.id}",
  "${field}": ${JSON.stringify(proposedVal)}
}
\`\`\``;
  }

  function updatePatchPreview() {
    if (!activeToolForEdit) return;
    const field = editFieldSelect.value;

    if (field === 'remove') {
      editPatchPreview.innerHTML = `// Tool Removal Proposal
{
  "id": "${activeToolForEdit.id}",
<span style="color: #ef4444;">- "action": "KEEP"</span>
<span style="color: #22c55e;">+ "action": "REMOVE"</span>
}`;
      return;
    }

    let currentVal = activeToolForEdit[field];
    if (currentVal === undefined || currentVal === null) {
      currentVal = null;
    }
    const proposedVal = editProposedValue.value.trim();
    
    if (!proposedVal) {
      editPatchPreview.innerHTML = `<span style="color: var(--text-muted); font-style: italic;">Enter proposed value to view patch preview...</span>`;
      return;
    }

    const diffHtml = `// JSON Patch Proposal
{
  "id": "${activeToolForEdit.id}",
<span style="color: #ef4444;">- "${field}": ${JSON.stringify(currentVal)}</span>
<span style="color: #22c55e;">+ "${field}": ${JSON.stringify(proposedVal)}</span>
}`;
    editPatchPreview.innerHTML = diffHtml;
  }

  if (btnSubmitGithubIssue) {
    btnSubmitGithubIssue.addEventListener('click', () => {
      const field = editFieldSelect.value;
      if (field !== 'remove') {
        const proposedVal = editProposedValue.value.trim();
        if (!proposedVal) {
          alert('Please enter a proposed corrected value.');
          return;
        }
      }
      
      const markdown = generateProposalMarkdown();
      const title = field === 'remove'
        ? `[Data Removal] Remove tool/method: ${activeToolForEdit.name} (${activeToolForEdit.id})`
        : `[Data Correction] Update ${editFieldSelect.options[editFieldSelect.selectedIndex].text} for ${activeToolForEdit.name}`;
      const url = `https://github.com/KarelBerka/alphafoldology/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(markdown)}`;
      window.open(url, '_blank');
    });
  }

  if (btnCopyEditJson) {
    btnCopyEditJson.addEventListener('click', () => {
      if (!activeToolForEdit) return;
      const evidence = editEvidence.value.trim();
      const title = `[Data Removal] Remove tool/method: ${activeToolForEdit.name} (${activeToolForEdit.id})`;
      const markdown = `### Tool/Method Removal Request

- **Tool/Method Name:** ${activeToolForEdit.name} (ID: \`${activeToolForEdit.id}\`)
- **Action:** Requesting removal of this entire tool entry from the database.
- **GitHub Repository:** ${activeToolForEdit.repo ? `https://github.com/${activeToolForEdit.repo}` : 'N/A'}
- **Reason for Removal / Evidence:** ${evidence ? evidence : 'No reason provided. Please add context here.'}

---
Proposed action: Delete the JSON object for \`${activeToolForEdit.id}\` from \`tools_data.json\`.`;

      const url = `https://github.com/KarelBerka/alphafoldology/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(markdown)}`;
      window.open(url, '_blank');
    });
  }

  // Search & filter listeners
  searchInput.addEventListener('input', (e) => {
    currentFilters.search = e.target.value;
    filterAndRenderContent();
  });

  categoryChips.addEventListener('click', (e) => {
    const chipBtn = e.target.closest('.chip');
    if (chipBtn) {
      // Toggle active chip
      categoryChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chipBtn.classList.add('active');
      
      currentFilters.category = chipBtn.getAttribute('data-category');
      filterAndRenderContent();
    }
  });

  pubChips.addEventListener('click', (e) => {
    const chipBtn = e.target.closest('.chip');
    if (chipBtn) {
      // Toggle active chip
      pubChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chipBtn.classList.add('active');
      
      currentFilters.pub = chipBtn.getAttribute('data-pub');
      filterAndRenderContent();
    }
  });

  sortChips.addEventListener('click', (e) => {
    const chipBtn = e.target.closest('.chip');
    if (chipBtn) {
      // Toggle active chip
      sortChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chipBtn.classList.add('active');
      
      currentFilters.sort = chipBtn.getAttribute('data-sort');
      filterAndRenderContent();
    }
  });

  // View Mode Toggles
  btnViewGrid.addEventListener('click', () => {
    btnViewGrid.classList.add('active');
    btnViewTable.classList.remove('active');
    toolsGrid.style.display = 'grid';
    tableViewWrapper.style.display = 'none';
    activeView = 'grid';
  });

  btnViewTable.addEventListener('click', () => {
    btnViewTable.classList.add('active');
    btnViewGrid.classList.remove('active');
    toolsGrid.style.display = 'none';
    tableViewWrapper.style.display = 'block';
    activeView = 'table';
    setTimeout(updateFloatingScrollbar, 50);
  });

  // Floating Scrollbar Synchronization Logic
  function updateFloatingScrollbar() {
    if (floatingScrollbarInner && toolsTable) {
      floatingScrollbarInner.style.width = toolsTable.offsetWidth + 'px';
    }
  }

  if (floatingScrollbar && toolsTableContainer) {
    let isSyncingLeft = false;
    let isSyncingRight = false;
    
    floatingScrollbar.addEventListener('scroll', () => {
      if (!isSyncingLeft) {
        isSyncingRight = true;
        toolsTableContainer.scrollLeft = floatingScrollbar.scrollLeft;
      }
      isSyncingLeft = false;
    });
    
    toolsTableContainer.addEventListener('scroll', () => {
      if (!isSyncingRight) {
        isSyncingLeft = true;
        floatingScrollbar.scrollLeft = toolsTableContainer.scrollLeft;
      }
      isSyncingRight = false;
    });
    
    window.addEventListener('resize', updateFloatingScrollbar);
  }

  // Zoom and Pan Handlers for SVG Tree targeting the #viewport-group
  function applyTransform() {
    viewportGroup.style.transform = `translate(${panX}px, ${panY}px) scale(${zoomScale})`;
    
    // Toggle visibility of minor tools depending on zoomScale
    if (zoomScale >= 1.25) {
      svgTree.classList.add('show-minor');
    } else {
      svgTree.classList.remove('show-minor');
    }
  }

  function fitViewToMajorNodes() {
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    let count = 0;

    Object.keys(NODE_COORDINATES).forEach(key => {
      if (MAJOR_TOOL_IDS.has(key)) {
        const node = NODE_COORDINATES[key];
        if (node.x < minX) minX = node.x;
        if (node.x > maxX) maxX = node.x;
        if (node.y < minY) minY = node.y;
        if (node.y > maxY) maxY = node.y;
        count++;
      }
    });

    if (count === 0) return;

    // Add padding around the bounding box
    const padding = 80;
    const bboxWidth = (maxX - minX) + padding * 2;
    const bboxHeight = (maxY - minY) + padding * 2;

    const containerWidth = treeCanvas.clientWidth || 1200;
    const containerHeight = treeCanvas.clientHeight || 350;

    // Calculate scale to fit container
    const scaleX = containerWidth / bboxWidth;
    const scaleY = containerHeight / bboxHeight;
    zoomScale = Math.min(scaleX, scaleY);
    zoomScale = Math.max(0.15, Math.min(2.0, zoomScale)); // Clamp scale to protect zoom ranges

    // Center the bounding box
    const centerX = minX + (maxX - minX) / 2;
    const centerY = minY + (maxY - minY) / 2;

    panX = containerWidth / 2 - centerX * zoomScale;
    panY = containerHeight / 2 - centerY * zoomScale;

    applyTransform();
  }

  document.getElementById('btn-zoom-in').addEventListener('click', () => {
    zoomScale = Math.min(zoomScale + 0.15, 2.5);
    applyTransform();
  });

  document.getElementById('btn-zoom-out').addEventListener('click', () => {
    zoomScale = Math.max(zoomScale - 0.15, 0.5);
    applyTransform();
  });

  document.getElementById('btn-reset-zoom').addEventListener('click', () => {
    fitViewToMajorNodes();
  });

  // Expand / collapse map canvas toggle
  const btnExpandTree = document.getElementById('btn-expand-tree');
  const treeViewportContainer = document.querySelector('.tree-viewport-container');
  btnExpandTree.addEventListener('click', () => {
    const isExpanded = treeViewportContainer.classList.toggle('expanded');
    btnExpandTree.textContent = isExpanded ? 'Collapse Map' : 'Expand Map';
    setTimeout(fitViewToMajorNodes, 420);
  });

  window.addEventListener('resize', fitViewToMajorNodes);

  // Mouse wheel zoom support
  treeCanvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomIntensity = 0.05;
    const delta = e.deltaY < 0 ? 1 : -1;
    zoomScale = Math.max(0.5, Math.min(2.5, zoomScale + delta * zoomIntensity));
    applyTransform();
  }, { passive: false });

  treeCanvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX - panX;
    startY = e.clientY - panY;
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  treeCanvas.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    panX = e.clientX - startX;
    panY = e.clientY - startY;
    applyTransform();
  });
});
