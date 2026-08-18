import { cn } from '../../utils/cn'

export function Skeleton({ className, ...props }) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-md bg-surface-subtle motion-reduce:animate-none',
        className,
      )}
      aria-hidden="true"
      {...props}
    />
  )
}

export function SkeletonCard({ lines = 3 }) {
  return (
    <div className="surface-card space-y-3 p-4">
      <Skeleton className="h-4 w-1/3" />
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton key={i} className={cn('h-3', i === lines - 1 ? 'w-2/3' : 'w-full')} />
      ))}
    </div>
  )
}

export function SkeletonChatBubble({ isUser = false }) {
  return (
    <div className={cn('flex', isUser ? 'justify-end' : 'justify-start')}>
      <Skeleton className={cn('h-16 rounded-xl', isUser ? 'w-2/3' : 'w-3/4')} />
    </div>
  )
}
