(ns mrs-doyle.core
  (:require [quit-yo-jibber :refer :all]
            [clojure.string :refer [split capitalize join]]
            [clojure.set :refer [intersection difference union]])
  (:gen-class))

(defn password-info []
  (read-string (slurp "credentials.clj")))

(defn salutation
  "Takes an email address, for example \"adam.clements@gmail.com\"
   and turns it into an appropriate salutation, e.g. \"Adam Clements\" "
  [email]
  (let [name  (first (split email #"@"))
        parts (split name #"\.")]
    (join " "(map capitalize parts))))

(defn like-drinking-tea []
  ;;STUB
  ["adam@swiftkey.net", "adam.clements@gmail.com"])

(defn potential-drinkers [conn from]
  (remove #{from} (intersection (like-drinking-tea) (online conn))))

(defn greeting [conn msg]
  (when (re-find #"[hH]ello" (:body msg))
    "Well hello to you too"))

(defn tea-prompt [conn msg]
  (when (re-find #"[tT]ea" (:body msg))
    (doseq [drinker (potential-drinkers conn (:from msg))]
      (send-message conn drinker "Will you have a cup of tea?"))
    "Yes! Let's have some tea!"))

(defn sweary [conn msg]
  (when (re-find #"carp" (:body msg))
    "Wash your mouth out young sir!"))

(defn command-chain [conn message]
  (some #(% conn message) [tea-prompt
                           sweary
                           greeting
                           (constantly "Umm")]))

(defn new-bot []
  (make-connection
   (password-info) :message (var command-chain)))

(defn -main [& args]
  (new-bot)
  (println "I'm awake!")
  (doseq [line (read-line)]))










