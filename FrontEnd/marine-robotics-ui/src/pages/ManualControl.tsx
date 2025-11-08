export default function ManualControl() {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="card">
        <h2 className="font-semibold mb-3">Pilot Controls</h2>
        <div className="space-y-3 text-white/80 text-sm">
          <div className="flex items-center justify-between">
            <span>Throttle</span>
            <input type="range" className="w-56" disabled />
          </div>
          <div className="flex items-center justify-between">
            <span>Yaw</span>
            <input type="range" className="w-56" disabled />
          </div>
          <div className="flex items-center justify-between">
            <span>Pitch</span>
            <input type="range" className="w-56" disabled />
          </div>
          <div className="flex items-center justify-between">
            <span>Roll</span>
            <input type="range" className="w-56" disabled />
          </div>
          <div className="text-white/60 text-xs">Connect your control back-end to enable inputs.</div>
        </div>
      </div>
      <div className="card">
        <h2 className="font-semibold mb-3">Camera Feed</h2>
        <div className="aspect-video bg-black/40 rounded-lg grid place-items-center text-white/70">
          Live camera feed placeholder
        </div>
      </div>
    </div>
  );
}
