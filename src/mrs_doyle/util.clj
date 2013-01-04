(ns mrs-doyle.util
  (:require [clojure.string :refer [split join capitalize]]))

(defmacro make-command-chain
  "Builds up a command chain, pass in pairs of message regex and function"
  [& body]
  `(fn [conn# message#]
     ((condp re-find (:body message#) ~@body) conn# message#)))

(defn salutation
  "Takes an email address, for example \"adam.clements@gmail.com\"
   and turns it into an appropriate salutation, e.g. \"Adam Clements\" "
  [email]
  (let [name  (first (split email #"@"))
        parts (split name #"\.")]
    (join " "(map capitalize parts))))
