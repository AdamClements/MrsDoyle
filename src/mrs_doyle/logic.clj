(ns mrs-doyle.logic
  (:require [mrs-doyle.util :refer :all]
            [quit-yo-jibber :as xmpp]
            [clojure.set :refer [intersection difference union]]
            [mrs-doyle.conversation :as conv]))

(defn like-drinking-tea []
  #{"adam@swiftkey.net", "adam.clements@gmail.com"})

(defn potential-drinkers [conn from]
  (disj (intersection (set (like-drinking-tea))
                      (set (xmpp/online conn)))
        from))

(defn greeting [conn msg]
  "Well hello to you too")

(defn tea-prompt [conn msg]
  (doseq [drinker (potential-drinkers conn (:from msg))]
    (xmpp/send-message conn drinker "Will you have a cup of tea?"))
  "Yes! Let's have some tea!")

(defn sweary [conn msg]
  "Wash your mouth out young sir!")

(def command-chain
  (make-command-chain #"[Tt]ea"   tea-prompt
                      #"crap"     sweary
                      #"[hH]ello" greeting
                      (constantly "Ummmm")))

(defn reply [msg] ())

(defn decision-tree [conn msg]
  (let [said    (:body msg)
        speaker (:from msg)]
    (cond (round-running) (cond
                           (conv/yes? said) (add-to-round! speaker)
                           :else            (conv/ah-go-on))
          :else           (cond
                           (conv/tea? said) (have-tea! conn speaker)
                           (conv/hello?)    (conv/hello)))))
