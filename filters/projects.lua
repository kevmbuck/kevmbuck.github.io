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
function Div(div)
  if not div.classes:includes("project-catalog") then return nil end
  local data_path = div.attributes["data"]
  local requested_kind = div.attributes["kind"]
  if not data_path then error("project-catalog requires a data attribute") end
  local projects = read_yaml_sequence(data_path)
  local cards = {}
  for _, project in ipairs(projects) do
    local kind_matches = not requested_kind or stringify(project.kind) == requested_kind
    if kind_matches then
      local links = {}
      for _, key in ipairs({"github", "paper", "documentation", "demo"}) do
        local href = project.links and project.links[key]
        if href and stringify(href) ~= "" then
          local label = ({github="GitHub", paper="Paper", documentation="Documentation", demo="Demo"})[key]
          table.insert(links, string.format('<a href="%s">%s</a>', escape_html(href), label))
        end
      end
      local tags = {}
      for _, tag in ipairs(project.tags or {}) do table.insert(tags, '<span class="project-tag">' .. escape_html(tag) .. '</span>') end
      table.insert(cards, pandoc.RawBlock("html", string.format([[<article class="project-card" id="%s"><h3>%s</h3><p>%s</p><div class="project-tags">%s</div>%s</article>]], escape_html(project.id), escape_html(project.title), escape_html(project.summary), table.concat(tags, ""), #links > 0 and ('<div class="project-links">' .. table.concat(links, " · ") .. '</div>') or "")))
    end
  end
  if #cards == 0 then return {pandoc.Para({pandoc.Str("Public software links will be added as projects are prepared for release.")})} end
  return {pandoc.Div(cards, pandoc.Attr("", {"project-grid"}))}
end
