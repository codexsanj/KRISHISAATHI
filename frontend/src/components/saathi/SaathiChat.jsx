import { useState, useRef, useEffect } from 'react'
import { Sparkles, Send, Leaf } from 'lucide-react'
import { cn } from '../../utils/cn'
import { Button } from '../common/Button'
import { SkeletonChatBubble } from '../common/Skeleton'
import { getSaathiMockResponse, SAATHI_SUGGESTED_PROMPTS } from '../../data/demoData'
import { useApp } from '../../stores/AppProvider'

function SaathiMessage({ message, isUser }) {
  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-xl rounded-br-sm bg-forest px-4 py-3 text-sm text-text-inverse">
          {message.text}
        </div>
      </div>
    )
  }

  return (
    <div className="flex gap-2.5">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-sage-bg text-forest ring-1 ring-sage/30">
        <Leaf className="h-4 w-4" aria-hidden="true" />
      </div>
      <div className="min-w-0 max-w-[85%] space-y-2">
        <div className="rounded-xl rounded-tl-sm border border-sage/20 bg-surface px-4 py-3 shadow-xs">
          {message.structured ? (
            <div className="space-y-2.5 text-sm">
              <div>
                <p className="text-label mb-0.5 text-forest">What</p>
                <p className="text-text">{message.structured.what}</p>
              </div>
              <div>
                <p className="text-label mb-0.5 text-forest">When</p>
                <p className="text-text">{message.structured.when}</p>
              </div>
              <div>
                <p className="text-label mb-0.5 text-forest">Why</p>
                <p className="text-text-muted">{message.structured.why}</p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-text">{message.text}</p>
          )}
        </div>
        {message.isDemo && (
          <p className="text-[10px] text-text-subtle">Demo response — not connected to real AI yet</p>
        )}
      </div>
    </div>
  )
}

export function SaathiChat({ compact = false }) {
  const { farmer, farm } = useApp()
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      isUser: false,
      text: null,
      structured: null,
      isWelcome: true,
    },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const bottomRef = useRef(null)

  const farmerName = farmer?.name?.trim()
  const greeting = farmerName ? `Hi ${farmerName}!` : 'Hi!'
  const cropContext = farm?.crop ? `your ${farm.crop}` : 'your crop'

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const sendMessage = (text) => {
    const trimmed = text.trim()
    if (!trimmed || isTyping) return

    setMessages((prev) => [
      ...prev,
      { id: `user-${Date.now()}`, isUser: true, text: trimmed },
    ])
    setInput('')
    setIsTyping(true)

    setTimeout(() => {
      const response = getSaathiMockResponse(trimmed, farm)
      setMessages((prev) => [
        ...prev,
        {
          id: `saathi-${Date.now()}`,
          isUser: false,
          structured: response,
          isDemo: true,
        },
      ])
      setIsTyping(false)
    }, 900)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(input)
  }

  return (
    <div
      className={cn(
        'flex flex-col overflow-hidden rounded-xl border border-sage/25 bg-surface shadow-sm',
        compact ? 'h-[420px]' : 'h-[calc(100dvh-12rem)] min-h-[480px] max-h-[700px]',
      )}
    >
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-border bg-sage-bg/40 px-4 py-3">
        <div className="saathi-glow flex h-9 w-9 items-center justify-center rounded-lg bg-forest text-text-inverse">
          <Sparkles className="h-4 w-4" aria-hidden="true" />
        </div>
        <div className="min-w-0">
          <p className="font-semibold text-text">Saathi</p>
          <p className="text-xs text-text-muted">Your farming companion</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 space-y-4 overflow-y-auto overscroll-contain px-4 py-4">
        {/* Welcome message */}
        <div className="flex gap-2.5">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-sage-bg text-forest ring-1 ring-sage/30">
            <Leaf className="h-4 w-4" aria-hidden="true" />
          </div>
          <div className="max-w-[90%] rounded-xl rounded-tl-sm border border-sage/20 bg-sage-bg/50 px-4 py-3">
            <p className="text-sm font-medium text-text">
              {greeting} I&apos;m Saathi
            </p>
            <p className="mt-1.5 text-sm text-text-muted">
              I can help you understand {cropContext}, weather, irrigation and today&apos;s farm tasks.
            </p>
          </div>
        </div>

        {messages.filter((m) => !m.isWelcome).map((msg) => (
          <SaathiMessage key={msg.id} message={msg} isUser={msg.isUser} />
        ))}

        {isTyping && <SkeletonChatBubble />}

        <div ref={bottomRef} />
      </div>

      {/* Suggested prompts */}
      <div className="border-t border-border bg-surface-muted/50 px-3 py-2.5">
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
          {SAATHI_SUGGESTED_PROMPTS.map((prompt) => (
            <button
              key={prompt}
              type="button"
              onClick={() => sendMessage(prompt)}
              disabled={isTyping}
              className="shrink-0 rounded-full border border-sage/30 bg-surface px-3 py-1.5 text-xs font-medium text-forest transition-colors hover:bg-sage-bg disabled:opacity-50"
            >
              {prompt}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-2 border-t border-border px-3 py-3"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Saathi about your farm…"
          className="input-field flex-1"
          disabled={isTyping}
          aria-label="Message to Saathi"
        />
        <Button
          type="submit"
          size="icon"
          disabled={!input.trim() || isTyping}
          aria-label="Send message"
        >
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </div>
  )
}
