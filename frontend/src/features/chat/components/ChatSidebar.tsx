"use client"

import { AnimatePresence, motion } from "framer-motion"
import { LogOut, MessageSquarePlus, Trash2 } from "lucide-react"
import { useRouter } from "next/navigation"

import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { displayNameFromEmail, useAuth } from "@/features/auth/context"
import type { ChatConversation } from "@/features/chat/types"
import type { ApiStatus } from "@/features/system/hooks/useApiStatus"
import { cn } from "@/lib/utils"

type ChatSidebarProps = {
  conversations: ChatConversation[]
  activeConversationId: string | null
  apiStatus: ApiStatus
  onNewConversation: () => Promise<void> | void
  onSelectConversation: (conversationId: string) => void
  onDeleteConversation: (conversationId: string) => Promise<void> | void
  onNavigate?: () => void
}

function ApiDot({ status }: { status: ApiStatus }) {
  const color =
    status === "connected"
      ? "bg-emerald-500"
      : status === "checking"
        ? "bg-amber-400"
        : "bg-red-500"
  const title =
    status === "connected"
      ? "API online"
      : status === "checking"
        ? "Verificando API..."
        : "API offline"
  return (
    <span
      title={title}
      role="img"
      aria-label={title}
      className={cn("inline-block h-2 w-2 shrink-0 rounded-full", color)}
    />
  )
}

export function ChatSidebar({
  conversations,
  activeConversationId,
  apiStatus,
  onNewConversation,
  onSelectConversation,
  onDeleteConversation,
  onNavigate,
}: ChatSidebarProps) {
  const { session, logout } = useAuth()
  const router = useRouter()

  function handleLogout() {
    logout()
    onNavigate?.()
    router.push("/login")
    router.refresh()
  }

  const label = session ? displayNameFromEmail(session.email) : ""

  return (
    <div className="flex h-full min-h-0 flex-col bg-[#0d0d0d]">
      <div className="shrink-0 space-y-3 p-3">
        <Button
          type="button"
          variant="secondary"
          className="h-11 w-full justify-start gap-2 rounded-lg bg-zinc-800/90 font-medium text-zinc-100 shadow-none hover:bg-zinc-700"
          onClick={() => void onNewConversation()}
        >
          <MessageSquarePlus className="h-4 w-4" />
          Nova conversa
        </Button>
      </div>

      <div className="px-3 pb-1">
        <p className="px-1 text-xs font-medium uppercase tracking-wide text-zinc-500">Recentes</p>
      </div>

      <div className="custom-scrollbar min-h-0 flex-1 space-y-0.5 overflow-y-auto px-2 pb-3">
        <AnimatePresence initial={false} mode="popLayout">
          {conversations.map((conversation) => {
            const isActive = conversation.id === activeConversationId

            return (
              <motion.div
                key={conversation.id}
                layout
                initial={{ opacity: 0, x: -6 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
                className={cn(
                  "group relative rounded-lg transition-colors",
                  isActive ? "bg-zinc-800/90" : "hover:bg-zinc-800/50",
                )}
              >
                <button
                  type="button"
                  onClick={() => {
                    onSelectConversation(conversation.id)
                    onNavigate?.()
                  }}
                  className="flex w-full min-w-0 cursor-pointer items-center gap-2 px-3 py-2.5 pr-10 text-left"
                >
                  <span className="truncate text-sm text-zinc-100">{conversation.title}</span>
                </button>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="absolute right-1 top-1/2 h-7 w-7 -translate-y-1/2 text-zinc-500 opacity-0 hover:bg-zinc-700/80 hover:text-zinc-200 group-hover:opacity-100"
                  aria-label="Apagar conversa"
                  title="Apagar conversa"
                  onClick={(e) => {
                    e.stopPropagation()
                    void onDeleteConversation(conversation.id)
                  }}
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
              </motion.div>
            )
          })}
        </AnimatePresence>
      </div>

      {session ? (
        <div className="mt-auto shrink-0 border-t border-white/5 p-3">
          <div className="flex items-center gap-3 rounded-lg px-1 py-1">
            <Avatar className="h-9 w-9 border border-white/10">
              <AvatarFallback className="bg-zinc-700 text-xs font-medium text-zinc-200">
                {(label.slice(0, 2) || session.email.slice(0, 2)).toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-zinc-100">{label}</p>
              <p className="truncate text-xs text-zinc-500" title={session.email}>
                {session.email}
              </p>
            </div>
            <div className="flex shrink-0 items-center gap-2">
              <ApiDot status={apiStatus} />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100"
                aria-label="Sair"
                title="Sair"
                onClick={handleLogout}
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
