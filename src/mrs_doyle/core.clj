(ns mrs-doyle.core
  (:require [xmpp-clj :as xmpp]))

(def connection-info {:username "mrs.doyle.teabot@gmail.com"
                      :password "mXA7oaC7"
                      :host     "talk.google.com"
                      :domain   "gmail.com"})

(defn greeting [message]
  (when (re-find #"[hH]ello" (:body message))
    "Well hello to you too"))

(defn tea-prompt [msg]
  (when (re-find #"[tT]ea" (:body msg))
    "Yes! Let's have some tea!"))

(defn sweary [msg]
  (when (re-find #"carp" (:body msg))
    "Wash your mouth out young sir!"))

(defn command-chain [message]
  (some #(% message) [tea-prompt
                      sweary
                      greeting
                      (constantly "Umm")]))
