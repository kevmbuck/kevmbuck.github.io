local stringify = pandoc.utils.stringify
local function read_yaml_sequence(path)
  local handle, open_error = io.open(path, "r")
  if not handle then
    error(string.format("Unable to open YAML data file %s: %s", path, open_error or "unknown error"))
  end

  local contents = handle:read("*a")
  handle:close()

  -- Pandoc parses YAML metadata natively. Wrapping the top-level sequence
  -- under a temporary key keeps this compatible across Quarto versions.
  local indented = "  " .. contents:gsub("\n", "\n  ")
  local document = pandoc.read("---\nitems:\n" .. indented .. "\n---\n", "markdown")
  local items = document.meta.items

  if not items then
    error(string.format("YAML data file %s did not contain a top-level sequence", path))
  end

  return items
end
local function escape_html(value)
  local text = stringify(value or "")
  text = text:gsub("&", "&amp;")
  text = text:gsub("<", "&lt;")
  text = text:gsub(">", "&gt;")
  text = text:gsub('"', "&quot;")
  text = text:gsub("'", "&#39;")
  return text
end
local function join_authors(authors)
  local names = {}
  for _, author in ipairs(authors or {}) do table.insert(names, escape_html(author)) end
  return table.concat(names, ", ")
end
local function render_links(links)
  local output = {}
  local labels = {arxiv="arXiv", journal="Journal", code="Code", project="Project"}
  for _, key in ipairs({"arxiv", "journal", "code", "project"}) do
    local href = links and links[key]
    if href and stringify(href) ~= "" then
      table.insert(output, string.format('<a href="%s">%s</a>', escape_html(href), labels[key]))
    end
  end
  if #output == 0 then return "" end
  return '<div class="publication-links">' .. table.concat(output, " · ") .. "</div>"
end
local function render_publication(publication)
  local note = publication.note and (", " .. escape_html(publication.note)) or ""
  local abstract = ""
  if publication.abstract and stringify(publication.abstract) ~= "" then
    abstract = '<details class="abstract"><summary>Abstract</summary><p>' .. escape_html(publication.abstract) .. '</p></details>'
  end
  local bibtex = ""
  if publication.bibtex and stringify(publication.bibtex) ~= "" then
    bibtex = '<details class="bibtex"><summary>BibTeX</summary><pre><code>' .. escape_html(publication.bibtex) .. '</code></pre></details>'
  end
  return pandoc.RawBlock("html", string.format([[<article class="publication-card" id="%s"><span class="status-badge">%s</span><h3>%s</h3><p class="publication-authors">%s</p><p class="publication-venue"><em>%s</em>, %s%s.</p>%s%s%s</article>]],
    escape_html(publication.id), escape_html(publication.status), escape_html(publication.title), join_authors(publication.authors), escape_html(publication.venue), escape_html(publication.year), note, render_links(publication.links), abstract, bibtex))
end
function Div(div)
  if div.classes:includes("publication-highlights") then
    local publications = read_yaml_sequence(div.attributes["data"] or "data/publications.yml")
    local blocks = {}
    for id in (div.attributes["ids"] or ""):gmatch("[^,]+") do
      local found = false
      for _, publication in ipairs(publications) do
        if stringify(publication.id) == id then
          local href = publication.links and (publication.links.arxiv or publication.links.journal)
          local note = publication.note and (", " .. escape_html(publication.note)) or ""
          table.insert(blocks, pandoc.RawBlock("html", string.format([[<article class="publication-item"><span class="status-badge">%s</span><h3><a href="%s">%s</a></h3><p class="publication-authors">%s</p><p class="publication-venue"><em>%s</em>, %s%s.</p></article>]], escape_html(publication.status), escape_html(href), escape_html(publication.title), join_authors(publication.authors), escape_html(publication.venue), escape_html(publication.year), note)))
          found = true
          break
        end
      end
      if not found then error("Unknown publication highlight ID: " .. id) end
    end
    return {pandoc.Div(blocks, pandoc.Attr("", {"publication-list"}))}
  end
  if not div.classes:includes("publication-catalog") then return nil end
  local data_path = div.attributes["data"]
  if not data_path then error("publication-catalog requires a data attribute") end
  local publications = read_yaml_sequence(data_path)
  local groups = {{status="accepted",heading="Accepted publications"},{status="submitted",heading="Submitted papers"},{status="preprint",heading="Preprints"}}
  local blocks = {}
  for _, group in ipairs(groups) do
    table.insert(blocks, pandoc.Header(2, group.heading))
    for _, publication in ipairs(publications) do
      if stringify(publication.status) == group.status then table.insert(blocks, render_publication(publication)) end
    end
  end
  return blocks
end
