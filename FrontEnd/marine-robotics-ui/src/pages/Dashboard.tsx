export default function Dashboard() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div className="card">
        <h2 className="font-semibold mb-2">Mission Status</h2>
        <div className="text-white/80 text-sm">No active missions. Connect your backend to display live status.</div>
      </div>
      <div className="card">
        <h2 className="font-semibold mb-2">Vehicle Telemetry</h2>
        <div className="text-white/80 text-sm">Depth, heading, battery, GPS... add your telemetry graphs here.</div>
      </div>
      <div className="card md:col-span-2">
        <h2 className="font-semibold mb-2">Recent Events</h2>
        <ul className="text-white/80 text-sm list-disc pl-5 space-y-1">
          <li>Template initialized. Awaiting data sources.</li>
          <li>Use websockets/REST to populate this feed.</li>
        </ul>
      </div>
    </div>
  );
}
