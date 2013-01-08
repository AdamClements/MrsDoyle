(ns mrs-doyle.logic
  (:require [mrs-doyle.util :refer :all]
            [quit-yo-jibber :as xmpp]
            [clojure.set :refer [intersection difference union]]
            [mrs-doyle.conversation :as conv]))


;; State based stuff
(defn round-running []
  false)

(defn add-to-round! [person] nil)

(defn have-tea! [conn speaker] nil)

(defn like-drinking-tea []
  #{"adam@swiftkey.net", "adam.clements@gmail.com"})

;; derived
(defn potential-drinkers [conn from]
  (-> (intersection (set (like-drinking-tea))
                    (set (xmpp/online conn)))
      (disj from)))

;; logic
(defn decision-tree [conn msg]
  (let [said    (:body msg)
        speaker (:from msg)]
    (cond (conv/rude? said) (conv/rude)
          (round-running)   (cond
                             (conv/yes? said) (add-to-round! speaker)
                             :else            (conv/ah-go-on))
          :else             (cond
                             (conv/tea? said) (have-tea! conn speaker)
                             (conv/hello?)    (conv/greeting)))))
