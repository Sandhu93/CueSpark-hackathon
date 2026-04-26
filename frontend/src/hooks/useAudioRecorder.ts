"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export type AudioRecorderState = "idle" | "recording" | "recorded" | "error";

export interface AudioRecording {
  blob: Blob;
  file: File;
  url: string;
  durationSeconds: number;
}

export function useAudioRecorder() {
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const startedAtRef = useRef<number | null>(null);
  const [state, setState] = useState<AudioRecorderState>("idle");
  const [recording, setRecording] = useState<AudioRecording | null>(null);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (state !== "recording") return;
    const timer = window.setInterval(() => {
      if (startedAtRef.current === null) return;
      setElapsedSeconds(Math.floor((Date.now() - startedAtRef.current) / 1000));
    }, 250);
    return () => window.clearInterval(timer);
  }, [state]);

  useEffect(() => {
    return () => {
      stopTracks();
      if (recording?.url) URL.revokeObjectURL(recording.url);
    };
  }, [recording?.url]);

  const start = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setError("This browser does not support microphone recording.");
      setState("error");
      return;
    }

    try {
      if (recording?.url) URL.revokeObjectURL(recording.url);
      setRecording(null);
      setError(null);
      chunksRef.current = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const mimeType = pickMimeType();
      const recorder = new MediaRecorder(
        stream,
        mimeType ? { mimeType } : undefined,
      );
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      };
      recorder.onstop = () => {
        const durationSeconds =
          startedAtRef.current === null
            ? elapsedSeconds
            : Math.max(1, Math.round((Date.now() - startedAtRef.current) / 1000));
        const type = recorder.mimeType || "audio/webm";
        const blob = new Blob(chunksRef.current, { type });
        const extension = type.includes("ogg") ? "ogg" : "webm";
        const file = new File([blob], `spoken-answer.${extension}`, { type });
        const url = URL.createObjectURL(blob);
        setRecording({ blob, file, url, durationSeconds });
        setElapsedSeconds(durationSeconds);
        setState("recorded");
        stopTracks();
      };
      recorder.onerror = () => {
        setError("Recording failed. Check microphone permissions and try again.");
        setState("error");
        stopTracks();
      };

      startedAtRef.current = Date.now();
      setElapsedSeconds(0);
      setState("recording");
      recorder.start();
    } catch (err) {
      setError(permissionErrorMessage(err));
      setState("error");
      stopTracks();
    }
  }, [elapsedSeconds, recording?.url]);

  const stop = useCallback(() => {
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state === "recording") {
      recorder.stop();
    }
  }, []);

  const reset = useCallback(() => {
    if (recording?.url) URL.revokeObjectURL(recording.url);
    setRecording(null);
    setElapsedSeconds(0);
    setError(null);
    setState("idle");
    chunksRef.current = [];
    startedAtRef.current = null;
    stopTracks();
  }, [recording?.url]);

  return {
    state,
    recording,
    elapsedSeconds,
    error,
    start,
    stop,
    reset,
  };

  function stopTracks() {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    mediaRecorderRef.current = null;
    startedAtRef.current = null;
  }
}

function pickMimeType() {
  if (typeof MediaRecorder === "undefined") return "";
  const candidates = ["audio/webm;codecs=opus", "audio/webm", "audio/ogg;codecs=opus"];
  return candidates.find((type) => MediaRecorder.isTypeSupported(type)) ?? "";
}

function permissionErrorMessage(err: unknown) {
  if (err instanceof DOMException && err.name === "NotAllowedError") {
    return "Microphone permission was denied. Allow microphone access to record a spoken answer.";
  }
  if (err instanceof DOMException && err.name === "NotFoundError") {
    return "No microphone was found on this device.";
  }
  return err instanceof Error ? err.message : "Unable to start microphone recording.";
}
