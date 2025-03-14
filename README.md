# Aquarienfischerkennung

## Aufbau des Projektes
- Neuronales Netz zur Fischerkennung: Subprojects/CNN/fish_recognition/main.ipynb
- Webscraper zur Datensammlung: Subprojects/Database/scraper.py
- Datensatz zusammengesetzt aus Webscraper Bildern und eigenen: Subprojects/Database/images
- Bildmanipulation zur künstlichen Erweiterung des Datensatzes: Subprojects/Database/image_augmentation.ipynb

## Starten des Projektes
- Ausführen von Subprojects/Database/image_augmentation.ipynb um die augmentierten Bilder zu erzeugen
  - ```aug_number = 3``` bestimmt wie viele "neue" Bilder aus einem erstellt werden mehr als 4 haben mein eigenes System überlastet, 4 funktioniert nicht immer aber manchmal daher 3 als höchster sicher laufender Wert
- Ausführen von Subprojects/CNN/fish_recognition/main.ipynb
  - ```
    hist = model.fit(train_images, train_labels_one_hot, epochs=5,
                 validation_data=(val_images, val_labels_one_hot),
                 callbacks=[tensorboard_callback])
    ```
  - 4-5 epochs hat sich als guter Wert heraus gestellt bevor es zu Overfitting kommt
- ```aug_number = 4``` und ```epochs = 5``` haben mit über 60% Genauigkeit das beste Ergebnis geliefert
