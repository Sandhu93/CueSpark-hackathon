"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export type VideoPreviewState =
  | "idle"
  | "requesting_permission"
  | "active"
  | "stopped"
  | "permission_denied"
  | "not_supported"
  | "error";

export function useVideoPreview() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [state, setState] = useState<VideoPreviewState>("idle");
  const [error, setError] = useState<string | null>(null);

  const stop = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    setState((current) => (current === "active" ? "stopped" : current));
  }, []);

  const start = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setState("not_supported");
      setError("This browser does not support camera preview.");
      return;
    }
    setState("requesting_permission");
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setState("active");
    } catch (err) {
      stop();
      if (err instanceof DOMException && err.name === "NotAllowedError") {
        setState("permission_denied");
        setError("Camera permission was denied.");
        return;
      }
      setState("error");
      setError(err instanceof Error ? err.message : "Unable to start camera preview.");
    }
  }, [stop]);

  useEffect(() => stop, [stop]);

  return { videoRef, state, error, start, stop };
}
