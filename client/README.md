# EcoVision NYC — Client

Next.js frontend for EcoVision NYC. Captures a photo from the browser webcam and sends
it to the backend's `POST /classify` endpoint, then shows how to sort the item under
NYC's DSNY/311 recycling, composting, and trash rules.

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). The app expects the backend
(see `../server`) running on `http://127.0.0.1:8000` by default — override this with
`NEXT_PUBLIC_API_BASE_URL` in a `.env.local` file if the backend runs elsewhere.
