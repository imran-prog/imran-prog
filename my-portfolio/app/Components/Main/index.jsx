"use client";
import { useEffect } from "react";
// Icons
import Image from "next/image";
// Animations
import ScrollMagic from "scrollmagic";
import anime from "animejs/lib/anime.es";

export default function Main() {
  return (
    <div className="Main-Canvas" id="main_canvas">
      <span>Underconstruction</span>
      <Image
        src="/Icons/mouseScroll.svg"
        alt="Scroll Down"
        width={25}
        height={40}
      />
    </div>
  );
}
