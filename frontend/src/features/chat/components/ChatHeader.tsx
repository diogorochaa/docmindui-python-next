"use client"

import { motion } from "framer-motion"
import { PanelLeft } from "lucide-react"

import { Button } from "@/components/ui/button"

type ChatHeaderProps = {
  onOpenSidebar?: () => void
}

export function ChatHeader({ onOpenSidebar }: ChatHeaderProps) {
  return (
    <motion.header
      layout
      className="flex shrink-0 items-center gap-2 border-b border-white/5 px-3 py-2.5 md:px-4"
      transition={{ duration: 0.2 }}
    >
      <Button
        type="button"
        variant="ghost"
        size="icon"
        className="h-9 w-9 text-zinc-400 hover:bg-white/5 hover:text-zinc-100 md:hidden"
        aria-label="Abrir menu"
        onClick={onOpenSidebar}
      >
        <PanelLeft className="h-5 w-5" />
      </Button>
      <div className="flex min-w-0 items-center gap-1">
        <span className="truncate text-sm font-semibold text-zinc-100">DocMind</span>
        <span className="text-zinc-600" aria-hidden>
          ▾
        </span>
      </div>
    </motion.header>
  )
}
