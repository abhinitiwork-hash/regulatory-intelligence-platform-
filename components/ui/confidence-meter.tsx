export function ConfidenceMeter({
  value,
  label = "Confidence"
}: {
  value: number;
  label?: string;
}) {
  const percent = Math.round(value * 100);

  return (
    <div className="confidence">
      <div className="confidence__meta">
        <span>{label}</span>
        <strong>{percent}%</strong>
      </div>
      <div className="confidence__track" aria-hidden="true">
        <span className="confidence__fill" style={{ width: `${percent}%` }} />
      </div>
    </div>
  );
}

