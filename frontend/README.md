# Frontend (DocMind AI)

Stack padrão: **Next.js 16**, **React 19**, **pnpm**, **Biome**, **shadcn/ui** (Radix + Tailwind), **Tailwind CSS v4**.

## Pré-requisitos

- Node.js 22+ (recomendado)
- [pnpm](https://pnpm.io/) — versão em [`package.json`](./package.json) (`packageManager`; use Corepack se preferir: `corepack enable`)

## Comandos

```bash
pnpm install
pnpm dev
pnpm run lint      # Biome
pnpm run format    # Biome
pnpm run typecheck
pnpm run test
pnpm build
```

Componentes shadcn: [`components.json`](./components.json) (CLI: `pnpm dlx shadcn@latest add <componente>`).
