(ns mrs-doyle.core
  (:require [quit-yo-jibber :refer :all]
            [clojure.string :refer [split capitalize join]]))

(defn password-info []
  (read-string (slurp "credentials.clj")))

(defn salutation [email]
  (let [name (first (split email #"@"))
        parts (split name #"\.")]
    (join " "(map capitalize parts))))

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

(defn new-bot []
  (make-connection
   (password-info) :message (var command-chain)))
