import { NavItem, NavKey } from "@/lib/types";

export function Sidebar({
  items,
  selected,
  onSelect
}: {
  items: NavItem[];
  selected: NavKey;
  onSelect: (key: NavKey) => void;
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <span className="sidebar__eyebrow">Nirnay Portal</span>
        <h1>Nirnay</h1>
        <p>Reviewer-controlled regulatory workflow automation for CDSCO Stage 1.</p>
      </div>

      <nav className="sidebar__nav" aria-label="Primary">
        {items.map((item) => {
          const active = item.id === selected;

          return (
            <button
              key={item.id}
              className={`sidebar__link ${active ? "sidebar__link--active" : ""}`}
              onClick={() => onSelect(item.id)}
              type="button"
            >
              <span className="sidebar__token">{item.shortLabel}</span>
              <span>
                <strong>{item.label}</strong>
                <small>{item.description}</small>
              </span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar__footnote">
        <strong>Positioning</strong>
        <p>Assistive AI only. Final determination remains with the CDSCO reviewer.</p>
      </div>
    </aside>
  );
}
