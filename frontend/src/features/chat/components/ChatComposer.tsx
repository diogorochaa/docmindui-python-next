"use client"

import { motion } from "framer-motion"
import { ArrowUp, Loader2, Plus } from "lucide-react"
import { useRef } from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

type ChatComposerProps = {
  variant: "hero" | "thread"
  input: string
  selectedFile: File | null
  loading: boolean
  feedbackMessage: string | null
  onInputChange: (value: string) => void
  onFileChange: (file: File | null) => void
  onSendMessage: () => Promise<void> | void
}

export function ChatComposer({
  variant,
  input,
  selectedFile,
  loading,
  feedbackMessage,
  onInputChange,
  onFileChange,
  onSendMessage,
}: ChatComposerProps) {
  const fileRef = useRef<HTMLInputElement>(null)

  const shell = cn(
    "flex w-full items-center gap-2 rounded-full border border-white/10 bg-zinc-900/80 p-1.5 pl-2 shadow-inner backdrop-blur-sm transition-shadow",
    variant === "hero" && "max-w-2xl",
    variant === "thread" && "max-w-3xl",
  )

  return (
    <motion.div
      layout
      className={cn(
        "w-full",
        variant === "thread" && "border-t border-white/5 bg-background/80 pt-3",
      )}
      transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
    >
      <div
        className={cn(
          "mx-auto flex w-full flex-col gap-2",
          variant === "thread" && "px-3 pb-4 md:px-6",
        )}
      >
        <div className={cn("mx-auto flex w-full justify-center", variant === "hero" && "px-2")}>
          <div className={shell}>
            <input
              ref={fileRef}
              type="file"
              className="sr-only"
              onChange={(e) => onFileChange(e.target.files?.[0] ?? null)}
              disabled={loading}
            />
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="h-9 w-9 shrink-0 rounded-full text-zinc-400 hover:bg-white/10 hover:text-zinc-100"
              disabled={loading}
              aria-label="Anexar arquivo"
              title="Anexar arquivo"
              onClick={() => fileRef.current?.click()}
            >
              <Plus className="h-5 w-5" />
            </Button>

            <Input
              value={input}
              onChange={(e) => onInputChange(e.target.value)}
              placeholder="Pergunte alguma coisa"
              className="min-w-0 flex-1 border-0 bg-transparent px-0 text-[15px] text-zinc-100 shadow-none outline-none placeholder:text-zinc-500 focus:border-transparent focus:outline-none focus-visible:border-transparent focus-visible:ring-0"
              disabled={loading}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  void onSendMessage()
                }
              }}
            />

            <Button
              type="button"
              size="icon"
              className="h-9 w-9 shrink-0 rounded-full"
              disabled={loading || (!input.trim() && !selectedFile)}
              aria-label="Enviar"
              onClick={() => void onSendMessage()}
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <ArrowUp className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>

        {selectedFile ? (
          <p className="mx-auto max-w-2xl truncate text-center text-xs text-zinc-500">
            {selectedFile.name}
          </p>
        ) : null}

        {feedbackMessage ? (
          <motion.p
            role="alert"
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center text-sm text-destructive"
          >
            {feedbackMessage}
          </motion.p>
        ) : null}
      </div>
    </motion.div>
  )
}
