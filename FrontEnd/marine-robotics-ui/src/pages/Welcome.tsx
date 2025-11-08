export default function Welcome() {
  return (
    <section className="grid gap-6 lg:grid-cols-2 items-center">
      <div className="space-y-4">
        <h1 className="text-3xl md:text-4xl font-bold leading-tight">Welcome to Marine Robotics UI</h1>
        <p className="text-white/80">
          A modern template for ocean robotics projects: visualize missions, control vehicles, and
          share knowledge. Start from here and plug your data streams and APIs.
        </p>
        <div className="flex gap-3">
          <a href="/dashboard" className="btn-primary">Go to Dashboard</a>
          <a href="/education" className="px-4 py-2 rounded-lg border border-white/20 text-white/90 hover:bg-white/10 transition">
            Learn More
          </a>
        </div>
      </div>
      <div className="card">
        <div className="aspect-video w-full rounded-lg bg-gradient-to-br from-ocean-500/60 to-kelp-500/40 flex items-center justify-center text-white/90">
          <div className="text-center p-6">
            <div className="text-6xl mb-2">🛥️</div>
            <div className="font-medium">Marine Robotics Visualization Placeholder</div>
            <div className="text-sm text-white/70">Plug in your live map or camera feed here.</div>
          </div>
        </div>
      </div>
    </section>
  );
}
