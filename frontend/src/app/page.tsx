'use client'

import { AnimatePresence, motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'
import { useState } from 'react'

import { AuthGuard } from '@/features/auth/components/AuthGuard'
import { ChatComposer } from '@/features/chat/components/ChatComposer'
import { ChatHeader } from '@/features/chat/components/ChatHeader'
import { ChatMessageList } from '@/features/chat/components/ChatMessageList'
import { ChatQuickActions } from '@/features/chat/components/ChatQuickActions'
import { ChatSidebar } from '@/features/chat/components/ChatSidebar'
import { useChat } from '@/features/chat/hooks/useChat'
import { useApiStatus } from '@/features/system/hooks/useApiStatus'
import { cn } from '@/lib/utils'

export default function Home() {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false)
  const {
    conversations,
    activeConversationId,
    messages,
    input,
    selectedFile,
    loading,
    historyLoading,
    feedbackMessage,
    setInput,
    setSelectedFile,
    createConversation,
    selectConversation,
    deleteConversation,
    sendMessage,
  } = useChat()
  const apiStatus = useApiStatus()

  const isEmptyThread = messages.length === 0

  return (
    <AuthGuard>
      <motion.div
        layout
        className="relative flex h-screen overflow-hidden bg-[#0a0a0a]"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      >
        <AnimatePresence>
          {mobileSidebarOpen ? (
            <motion.button
              type="button"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-40 cursor-pointer bg-black/60 md:hidden"
              aria-label="Fechar menu"
              onClick={() => setMobileSidebarOpen(false)}
            />
          ) : null}
        </AnimatePresence>

        <aside
          className={cn(
            'fixed inset-y-0 left-0 z-50 flex w-[min(100%,17.5rem)] flex-col border-r border-white/5 bg-[#0d0d0d] transition-transform duration-200 ease-out md:relative md:inset-auto md:z-0 md:translate-x-0',
            mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
          )}
        >
          <ChatSidebar
            conversations={conversations}
            activeConversationId={activeConversationId}
            apiStatus={apiStatus}
            onNewConversation={createConversation}
            onSelectConversation={selectConversation}
            onDeleteConversation={deleteConversation}
            onNavigate={() => setMobileSidebarOpen(false)}
          />
        </aside>

        <main className="flex min-h-0 min-w-0 flex-1 flex-col bg-[#0a0a0a]">
          <ChatHeader onOpenSidebar={() => setMobileSidebarOpen(true)} />

          {isEmptyThread ? (
            <div className="flex min-h-0 flex-1 flex-col">
              <div className="flex flex-1 flex-col items-center justify-center px-4 pt-6 text-center">
                <motion.div
                  className="max-w-xl"
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                >
                  <h2 className="text-2xl font-normal tracking-tight text-zinc-100 md:text-3xl">
                    No que você está trabalhando?
                  </h2>
                  <p className="mt-2 text-sm text-zinc-500">
                    Envie uma pergunta ou anexe um PDF para indexar e conversar com o DocMind.
                  </p>
                </motion.div>
              </div>

              <div className="shrink-0 space-y-6 px-2 pb-8">
                <ChatComposer
                  variant="hero"
                  input={input}
                  selectedFile={selectedFile}
                  loading={loading}
                  feedbackMessage={feedbackMessage}
                  onInputChange={setInput}
                  onFileChange={setSelectedFile}
                  onSendMessage={sendMessage}
                />
                <ChatQuickActions onPick={(prompt) => setInput(prompt)} />
              </div>
            </div>
          ) : (
            <div className="flex min-h-0 flex-1 flex-col">
              <div className="min-h-0 flex-1">
                <ChatMessageList messages={messages} loading={loading} />
              </div>
              <ChatComposer
                variant="thread"
                input={input}
                selectedFile={selectedFile}
                loading={loading}
                feedbackMessage={feedbackMessage}
                onInputChange={setInput}
                onFileChange={setSelectedFile}
                onSendMessage={sendMessage}
              />
            </div>
          )}
        </main>

        {historyLoading ? (
          <div
            className="absolute inset-0 z-100 flex items-center justify-center bg-[#0a0a0a]/85 backdrop-blur-[2px]"
            role="status"
            aria-live="polite"
            aria-busy="true"
            aria-label="Carregando histórico de conversas"
          >
            <div className="flex flex-col items-center gap-3">
              <Loader2 className="h-9 w-9 animate-spin text-zinc-400" aria-hidden />
              <p className="text-sm text-zinc-500">Carregando seu histórico…</p>
            </div>
          </div>
        ) : null}
      </motion.div>
    </AuthGuard>
  )
}
