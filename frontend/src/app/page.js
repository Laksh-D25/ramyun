"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";

export default function Home() {
  const [waitlistCount, setWaitlistCount] = useState(1);
  const waitlistTotal = 25;

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden font-sans">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/bg-clay.png"
          alt="Background"
          fill
          className="object-cover"
          priority
          quality={100}
        />
        {/* Overlay for better text readability */}
        <div className="absolute inset-0 bg-black/40" />
      </div>

      {/* Main Content */}
      <main className="relative z-10 flex flex-col items-center justify-center px-6 text-center">
        {/* Ramyun Bowl Image */}
        <div className="mb-8">
          <Image
            src="/bg-clay-nobg.png"
            alt="Ramyun Bowl"
            width={200}
            height={200}
            className="drop-shadow-2xl"
            priority
          />
        </div>

        {/* Hero Title */}
        <h1 className="mb-4 text-6xl font-bold tracking-tight text-white md:text-7xl lg:text-8xl">
          RAMYUN
        </h1>

        {/* Tagline */}
        <p className="mb-6 text-xl font-medium text-white md:text-2xl">
          Cook your perfect playlist.
        </p>

        {/* Description */}
        <p className="mb-10 max-w-2xl text-base leading-relaxed text-gray-200 md:text-lg">
          Ramyun is an invite-only music kitchen. Select your ingredients—artists,
          genres, and moods—and let our chef serve up a custom Spotify playlist
          perfectly spiced to your taste.
        </p>

        {/* Waitlist Counter */}
        <div className="mb-8 rounded-full border border-white/30 bg-white/10 px-6 py-2 backdrop-blur-sm">
          <p className="text-sm font-medium text-white">
            Join the waitlist:{" "}
            <span className="font-bold">
              {waitlistCount}/{waitlistTotal}
            </span>
          </p>
        </div>

        {/* Main CTA Button */}
        <Link
          href="/auth"
          className="mb-4 rounded-full bg-white px-8 py-4 text-lg font-semibold text-black transition-all hover:scale-105 hover:bg-gray-100 hover:shadow-xl"
        >
          Login with Spotify
        </Link>

        {/* Secondary Link */}
        <Link
          href="/waitlist"
          className="mb-6 text-sm font-medium text-white underline decoration-white/50 underline-offset-4 transition-all hover:decoration-white"
        >
          Don&apos;t have a table? Request Access.
        </Link>

        {/* GitHub Link */}
        <a
          href="https://github.com/yourusername/ramyun"
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-gray-300 transition-colors hover:text-white"
        >
          Check out the Repo 🚀
        </a>
      </main>

      {/* Footer */}
      <footer className="absolute bottom-6 z-10 text-center text-sm text-gray-400">
        Private Beta. v1.0.
      </footer>
    </div>
  );
}
