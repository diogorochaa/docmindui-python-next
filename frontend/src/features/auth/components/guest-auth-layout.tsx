"use client"

import { useRouter } from "next/navigation"
import { type ReactNode, useEffect } from "react"

import { useAuth } from "@/features/auth/context"

import { AuthFullscreenLoading } from "./auth-fullscreen-loading"

export function GuestAuthLayout({ children }: { children: ReactNode }) {
  const router = useRouter()
  const { session, ready } = useAuth()

  useEffect(() => {
    if (ready && session) {
      router.replace("/")
    }
  }, [ready, session, router])

  if (!ready) {
    return <AuthFullscreenLoading />
  }

  if (session) {
    return null
  }

  return children
}
