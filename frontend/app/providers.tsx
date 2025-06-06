'use client'

import posthog from 'posthog-js'
import { PostHogProvider as PHProvider } from 'posthog-js/react'
import { useEffect, useState } from 'react'

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  const [shouldUsePosthog, setShouldUsePosthog] = useState(false)

  const posthogKey = process.env.NEXT_PUBLIC_POSTHOG_KEY
  const posthogHost = process.env.NEXT_PUBLIC_POSTHOG_HOST

  useEffect(() => {
    if (posthogKey && posthogHost) {
      posthog.init(posthogKey, {
        api_host: posthogHost,
        capture_pageview: true,
        persistence: 'memory'
      })
      setShouldUsePosthog(true)
      console.log('PostHog initialized')
    }
  }, [posthogKey, posthogHost])

  if (!shouldUsePosthog) {
    return <>{children}</>
  }

  return (
    <PHProvider client={posthog}>
      {children}
    </PHProvider>
  )
}
