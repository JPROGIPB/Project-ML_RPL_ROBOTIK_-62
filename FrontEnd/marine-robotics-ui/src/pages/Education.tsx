export default function Education() {
  return (
    <div className="grid gap-6">
      <div className="card">
        <h2 className="font-semibold mb-2">Learning Modules</h2>
        <ul className="list-disc pl-6 space-y-1 text-white/85 text-sm">
          <li>Introduction to ROV/AUV basics</li>
          <li>Sensor fusion and navigation</li>
          <li>Underwater communication</li>
          <li>Mission planning and safety</li>
        </ul>
      </div>
      <div className="card">
        <h2 className="font-semibold mb-2">Resources</h2>
        <div className="text-white/80 text-sm">Link your docs, tutorials, and datasets here.</div>
      </div>
    </div>
  );
}
