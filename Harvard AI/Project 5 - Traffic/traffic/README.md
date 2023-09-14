## Initial Run

### What I tried:
I initially began this project by using the same values as in the lecture:
- 1 2D convolutional layer of 32 filters.
- 1 Max-pooling layer, using a 2x2 pool size.
- 1 dense hidden layer of 128 neurons.
- 1 dropout layer with a rate of 50%.

### What went wrong:
The accuracy presented was extremely low.
- It began at 0.0522 on epoch 1.
- It rose to 0.0565 on epoch 2. 
- For the next 7 epochs the accuracy remained at 0.0572.

The average accuracy of 5.49% was low, hence changes needed to be made.

## 1. Number of Convolutional Layers
- On my initial test, I had used a single convolutional layer, giving an accuracy of 5.49%.
- To improve this, I began by tweaking the number of convolutional layers.
### Results
- Number: 1 | Accuracy: 65.61%
- Number: 2 | Accuracy: 94.05%
- Number: 3 | Accuracy: 95.19%
- Number: 4 | Accuracy: 95.75%

### What I Noticed
- I identified a direct correlation between convolutional layers and accuracy.
- However, there was also a direct correlation with processing time and the number of layers.
- While more layers meant better accuracy, it also resulted in more time for the results.
- Since there wasn't a major difference between 2, 3 and 4 layers, I decided to use 2 convolutional layers.

## 2. Number of Filters
- On my initial test, I had used 32 filters.
- To try and get a better result, I experimented with different numbers of filters.
- The results below are obtained after adding 2 convolutional layers.

### Results
- Filters: 16 | Accuracy: 92.84%
- Filters: 32 | Accuracy: 94.05%
- Filters: 64 | Accuracy: 94.65%

### What I Noticed
- Accuracy is directly proportional to number of filters.
- 64 filters was only slightly more accurate than 32.
- However, it also took a lot more processing time than 32 filters.
- Hence, I decided to remain with 32 filters.

## 3. Sizes of Filters
- On my initial test, I had used a 3x3 kernel.
- To improve this, I tested different filter sizes.
- I used 2 convolutional layers.

### Results
- Kernel: (2, 2)  | Accuracy: 89.82%
- Kernel: (3, 3)  | Accuracy: 94.05%
- Kernel: (4, 4)  | Accuracy: 92.60%

Since a 3x3 kernel had the highest accuracy, I decided to remain with it.

## 4. Number of Pooling Layers
- On my initial test, I had used a single pooling layer.
- To improve this, I tested different numbers of pooling layers.
- I used 2 convolutional layers.

### Results
- Number: 1 | Accuracy: 94.05%
- Number: 2 | Accuracy: 95.73%

Hence, 2 pooling layers are more accurate than 1 alone.

## 5. Size of Pooling Layers
- On my initial test, I had used a pool size of (2,2)
- To improve this, I tested different sizes of pooling layers.
- I used 2 convolutional layers and 2 pooling layers.

### Results
- Number: (2,2) | Accuracy: 95.73%
- Number: (3,3) | Accuracy: 79.98%

Hence, a (2, 2) pool size is most accurate.

## 6. Number of Hidden Layers
- On my initial test, I had used one hidden layer.
- To improve this, I tested different numbers of hidden layers.
- I used 2 convolutional layers and 2 pooling layers.

### Results
- Number: 0 | Accuracy: 85.50%
- Number: 1 | Accuracy: 95.73%
- Number: 2 | Accuracy: 95.97%
- Number: 3 | Accuracy: 96.23%

### What I Noticed
- The number of hidden layers is directly proportional to an increase in accuracy.
- Incrementing the number of layers by 1 only increases the accuracy a small amount.
- However, the processing time also increases as the number of layers increases.
- Thus, I decided to remain with 1 hidden layer as it is the best trade-off for time with accuracy.

## 7. Size of Hidden Layers
- On my initial test, I had used 128 neurons.
- To improve this, I tested different numbers of neurons.
- I used 2 convolutional layers and 2 pooling layers.

### Results
- Number: 128 | Accuracy: 95.73%
- Number: 256 | Accuracy: 96.37%
- Number: 512 | Accuracy: 96.62%

### What I Noticed
- While using 256/512 neurons was a slightly more accurate than 128, the processing time taken was a lot more.
- For a slight increase in accuracy, a large decrease in speed isn't worth it, hence I decided to stick with 128 neurons.

## 8. Dropout
- On my initial test, I had used a dropout of 0.5.
- To improve this, I experimented with different dropout values.
- I used 2 convolutional layers and 2 pooling layers.

### Results:
- Dropout: 0.5  | Accuracy: 95.73%
- Dropout: 0.3  | Accuracy: 95.94%.
- Dropout: 0.1  | Accuracy: 96.23%.
- Dropout: 0.05 | Accuracy: 96.76%.

### What I Noticed
- As the dropout value decreased, the accuracy increased.
- However, at a dropout of 0.05, I noticed the problem of overfitting.
- While the accuracy during evaluation was 96.76%, Epoch 10 had a higher accuracy of 97.12%. 
- This meant that the training data had become too closely modelled, thus it would fail to generalize other new data.
- Hence, I chose a dropout of 0.1.

## Conclusion
To conclude, here are my final configurations:
- 2 2D convolutional layers of 32 filters.
- 2 Max-pooling layers, using 2x2 pool size.
- 1 dense hidden layer of 128 neurons.
- 1 dropout layer with a rate of 10%.