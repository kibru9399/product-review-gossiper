import matplotlib.pyplot as plt
def topic_vis(l2): 
  fig, axes = plt.subplots(2, 3, figsize=(6, 5))
  colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']
  # Plot horizontal bar charts for each topic
  for i, ((topic, prob), ax) in enumerate(zip(l2, axes.flat)):
      # Assign a color from the colormap
    ax.barh(topic, prob, color=colors[i])
    ax.set_xlabel('Probability')
    ax.set_ylabel('Words')
    ax.set_title(f"Topic {i+1}")
    # Adjust layout and display plot
  plt.tight_layout()
  plt.subplots_adjust(top=0.9)
  plt.show() 
  return plt