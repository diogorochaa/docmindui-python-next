"use server"

import { requestAiAnswer, requestDocumentUpload } from "@/features/chat/api"

export async function askAiAction(question: string): Promise<string> {
  const trimmed = question.trim()
  if (!trimmed) {
    throw new Error("Pergunta vazia.")
  }

  return requestAiAnswer(trimmed)
}

export async function uploadDocumentAction(file: File): Promise<void> {
  if (!file) {
    throw new Error("Arquivo inválido.")
  }

  await requestDocumentUpload(file)
}
