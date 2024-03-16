import "./styles.css";
import "ninja-keys";
import { useState, useRef, useEffect } from "react";

export default function App() {
  const ninjaKeys = useRef(null);
  const [hotkeys, setHotkeys] = useState([
    {
      id: "Home",
      title: "Open Home",
      hotkey: "cmd+h",
      mdIcon: "home",
      handler: () => {
        console.log("navigation to home");
      }
    },
    {
      id: "Open Projects",
      title: "Open Projects",
      hotkey: "cmd+p",
      mdIcon: "apps",
      handler: () => {
        console.log("navigation to projects");
      }
    },
    {
      id: "Theme",
      title: "Change theme...",
      mdIcon: "desktop_windows",
      children: [
        {
          id: "Light Theme",
          title: "Change theme to Light",
          mdIcon: "light_mode",
          handler: () => {
            console.log("theme light");
          }
        },
        {
          id: "Dark Theme",
          title: "Change theme to Dark",
          mdIcon: "dark_mode",
          keywords: "lol",
          handler: () => {
            console.log("theme dark");
          }
        }
      ]
    }
  ]);

  useEffect(() => {
    if (ninjaKeys.current) {
      ninjaKeys.current.data = hotkeys;
    }
  }, []);

  return (
    <div >
      <h1>Hello from Ninja Keys</h1>
      <h2>Hit "Cmd+K" or "Ctrl+K"</h2>
      <h3>Actions logged to console in demo</h3>
      <ninja-keys ref={ninjaKeys}></ninja-keys>
    </div>
  );
}
