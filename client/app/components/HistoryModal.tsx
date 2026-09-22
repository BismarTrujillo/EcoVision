"use client";

import { useEffect } from "react";
import { History, Leaf, Recycle, Trash2, X } from "lucide-react";
import { HistoryLog } from "../types";

interface HistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  history: HistoryLog[];
}

export default function HistoryModal({ isOpen, onClose, history }: HistoryModalProps) {
  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-zinc-950/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Scan history"
        onClick={(e) => e.stopPropagation()}
        className="bg-zinc-900 border border-zinc-800 rounded-3xl w-full max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
      >
        <div className="flex items-center justify-between p-6 border-b border-zinc-800">
          <h3 className="font-semibold text-lg flex items-center gap-2">
            <History className="w-5 h-5 text-zinc-400" />
            Scan History
          </h3>
          <button
            onClick={onClose}
            aria-label="Close"
            className="p-1.5 rounded-full text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-4 overflow-y-auto">
          {history.length === 0 ? (
            <p className="text-zinc-500 text-sm text-center py-8">No scans yet.</p>
          ) : (
            history.map((log) => (
              <div
                key={log.id}
                className="flex items-center justify-between p-3 rounded-2xl bg-zinc-950/50 hover:bg-zinc-800/50 transition-colors border border-zinc-800/30"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`p-2 rounded-xl ${
                      log.category === "Recycle"
                        ? "bg-blue-500/20 text-blue-400"
                        : log.category === "Compost"
                        ? "bg-amber-500/20 text-amber-400"
                        : "bg-zinc-800 text-zinc-400"
                    }`}
                  >
                    {log.category === "Recycle" ? (
                      <Recycle className="w-4 h-4" />
                    ) : log.category === "Compost" ? (
                      <Leaf className="w-4 h-4" />
                    ) : (
                      <Trash2 className="w-4 h-4" />
                    )}
                  </div>
                  <div>
                    <p className="font-medium text-sm text-zinc-200">{log.item}</p>
                    <p className="text-xs text-zinc-500">{log.time}</p>
                  </div>
                </div>
                <span
                  className={`text-sm font-semibold ${
                    log.co2 !== "0.00" ? "text-emerald-400" : "text-zinc-500"
                  }`}
                >
                  {log.co2 !== "0.00" ? `${log.co2} kg` : "0 kg"}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
