"use client"

import { motion } from "framer-motion"
import { Globe, ImageIcon, PenLine } from "lucide-react"

import { Button } from "@/components/ui/button"

const items: { icon: typeof PenLine; label: string; prompt: string }[] = [
  {
    icon: ImageIcon,
    label: "Ideias visuais",
    prompt: "Sugira ideias visuais para ",
  },
  {
    icon: PenLine,
    label: "Escrever ou editar",
    prompt: "Ajude-me a escrever ou revisar o seguinte texto: ",
  },
  {
    icon: Globe,
    label: "Pesquisar tema",
    prompt: "Explique de forma objetiva: ",
  },
]

type ChatQuickActionsProps = {
  onPick: (prompt: string) => void
}

export function ChatQuickActions({ onPick }: ChatQuickActionsProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.08, duration: 0.3 }}
      className="mt-8 flex w-full max-w-2xl flex-wrap justify-center gap-2 px-2"
    >
      {items.map(({ icon: Icon, label, prompt }) => (
        <Button
          key={label}
          type="button"
          variant="outline"
          size="sm"
          className="rounded-full border-white/10 bg-zinc-900/50 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100"
          onClick={() => onPick(prompt)}
        >
          <Icon className="h-3.5 w-3.5" />
          {label}
        </Button>
      ))}
    </motion.div>
  )
}
