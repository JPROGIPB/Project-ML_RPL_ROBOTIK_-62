# Marine Robotics UI (Template)

Template React + TypeScript + Vite + TailwindCSS for a marine robotics themed app.

Pages included:
- Login
- Welcome (landing)
- Dashboard
- Manual Control
- Education

Routing is set up with a simple mock auth. After clicking Login, a flag is stored in localStorage to unlock protected routes.

## Requirements
- Node.js 18+
- npm 9+

## Quick start (Windows PowerShell)

```powershell
# From the project root
npm install
npm run dev
```

Open the URL shown (typically http://localhost:5173).

## Build & preview

```powershell
npm run build
npm run preview
```

## Structure
- `src/pages/*` page components
- `src/components/*` shared UI components
- `src/layouts/*` app layout (navbar + sidebar)

## Notes
- Tailwind oceanic theme is configured in `tailwind.config.js`.
- Replace placeholders with real data streams (REST/WebSocket) for telemetry, camera, and control.
- `ProtectedRoute` uses `localStorage['auth'] === 'true'` as a simple mock.
