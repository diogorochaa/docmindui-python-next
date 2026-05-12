"use client"

import { AnimatePresence, motion } from "framer-motion"
import { File, FileImage, FileText, Loader2 } from "lucide-react"

import { cn } from "@/lib/utils"
import type { ChatMessage } from "@/types/chat"

type ChatMessageListProps = {
  messages: ChatMessage[]
  loading: boolean
}

function attachmentIcon(kind: "pdf" | "image" | "file") {
  if (kind === "pdf") return <FileText className="h-3.5 w-3.5" />
  if (kind === "image") return <FileImage className="h-3.5 w-3.5" />
  return <File className="h-3.5 w-3.5" />
}

export function ChatMessageList({ messages, loading }: ChatMessageListProps) {
  return (
    <div className="custom-scrollbar flex h-full min-h-0 flex-1 flex-col overflow-y-auto">
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-6 md:px-6">
        <AnimatePresence initial={false} mode="popLayout">
          {messages.map((message) => (
            <motion.div
              key={[
                message.conversationId ?? "",
                message.role,
                message.createdAt ?? "",
                message.content,
                message.attachment?.name ?? "",
              ].join("|")}
              layout
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
              className={cn(
                "flex w-full",
                message.role === "user" ? "justify-end" : "justify-start",
              )}
            >
              <div
                className={cn(
                  "max-w-[85%] rounded-2xl px-4 py-3 text-[15px] leading-relaxed",
                  message.role === "user"
                    ? "bg-zinc-800 text-zinc-100"
                    : "bg-transparent px-0 text-zinc-100",
                )}
              >
                {message.attachment ? (
                  <div
                    className={cn(
                      "mb-2 flex items-center gap-2 rounded-xl px-2.5 py-2 text-xs font-medium",
                      message.attachment.kind === "pdf" &&
                        "bg-red-500/10 text-red-200 ring-1 ring-red-500/20",
                      message.attachment.kind === "image" &&
                        "bg-sky-500/10 text-sky-100 ring-1 ring-sky-500/20",
                      message.attachment.kind === "file" &&
                        "bg-zinc-800 text-zinc-300 ring-1 ring-white/10",
                    )}
                  >
                    <span
                      className={cn(
                        "flex h-7 w-7 shrink-0 items-center justify-center rounded-lg",
                        message.attachment.kind === "pdf" && "bg-red-600/30",
                        message.attachment.kind === "image" && "bg-sky-600/30",
                        message.attachment.kind === "file" && "bg-zinc-600/50",
                      )}
                    >
                      {attachmentIcon(message.attachment.kind)}
                    </span>
                    <span className="min-w-0 truncate">{message.attachment.name}</span>
                  </div>
                ) : null}
                {message.content ? (
                  <p className="whitespace-pre-wrap break-words text-zinc-100">{message.content}</p>
                ) : null}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {loading ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 text-sm text-zinc-500"
          >
            <Loader2 className="h-4 w-4 animate-spin" />
            Pensando...
          </motion.div>
        ) : null}
      </div>
    </div>
  )
}
