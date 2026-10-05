import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [
    react(),
    {
      name: "inject-ga4",
      transformIndexHtml(html) {
        return html.replace(
          "</head>",
          `<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GQLW7LNP6H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-GQLW7LNP6H');
</script>
</head>`
        );
      },
    },
  ],
  base: "/presentations/04-auspicious-date-guide/presentation/",
  server: {
    port: 5174,
    fs: { allow: [".."] },
  },
  build: {
    rollupOptions: {
      input: new URL("./index.src.html", import.meta.url).pathname,
    },
  },
});
