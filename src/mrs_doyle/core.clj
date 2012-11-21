(ns mrs-doyle.core
  (:require [quit-yo-jibber :refer :all]
            [mrs-doyle.logic :refer [command-chain]])
  (:gen-class))

(defn password-info []
  (read-string (slurp "credentials.clj")))

(defn new-bot []
  (make-connection (password-info) (var command-chain)))

(defn -main [& args]
  (new-bot)
  (println "I'm awake!")
  (doseq [line (read-line)]))
