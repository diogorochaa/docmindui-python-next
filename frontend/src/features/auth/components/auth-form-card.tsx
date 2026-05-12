"use client"

import { motion } from "framer-motion"
import type { ReactNode } from "react"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

const fadeUp = {
  initial: { opacity: 0, y: 14 },
  animate: { opacity: 1, y: 0 },
}

type AuthFormCardProps = {
  title: string
  description: string
  footer: ReactNode
  children: ReactNode
}

export function AuthFormCard({ title, description, footer, children }: AuthFormCardProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <motion.div
        className="w-full max-w-[420px]"
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      >
        <Card className="border-border shadow-lg">
          <CardHeader>
            <motion.div {...fadeUp} transition={{ duration: 0.3 }}>
              <CardTitle className="text-2xl font-bold tracking-tight">{title}</CardTitle>
              <CardDescription className="text-muted-foreground">{description}</CardDescription>
            </motion.div>
          </CardHeader>
          <CardContent>{children}</CardContent>
          <CardFooter className="flex flex-col gap-4">{footer}</CardFooter>
        </Card>
      </motion.div>
    </div>
  )
}
