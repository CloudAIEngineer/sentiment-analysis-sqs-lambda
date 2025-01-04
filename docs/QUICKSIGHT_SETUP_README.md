# QuickSight Setup Guide

This guide provides step-by-step instructions to set up a data source in Amazon QuickSight, create visuals, and design example charts for analyzing feedback data. Note that this guide will focus on setting up a typical data source and creating example charts. Additional charts can be designed following similar principles.

## 1. Set Up a Data Source
1. **Log in to QuickSight**: Navigate to the QuickSight dashboard.
2. **Create a New Data Set**:
   - Click on **Datasets** in the left-hand menu.
   - Choose **New Dataset**.
   - Select **Athena** as the data source type.
3. **Configure Athena**:
   - Enter a name for the data source, e.g., `FeedbackData`.
   - Choose your Athena Workgroup.
   - Click **Create Data Source**.
4. **Select the Database and Table**:
   - Choose the database created in Athena (e.g., `feedback_db`).
   - Select the table (e.g., `feedback_table`).
   - Click **Select**.
5. **Import or Query Data**:
   - Choose either **Import to SPICE for quicker analytics** (recommended for faster performance) or **Directly query your data**.
   - Click **Edit/Preview data** to finalize the schema.
6. **Save the Data Set**: Click **Save & visualize** to proceed to creating visuals.

## 2. Create Example Charts

### Example 1: Sentiment Proportion (Pie Chart)
1. **Add a Visual**:
   - Click **Add** > **Add visual**.
   - Select the **Pie Chart** type.
2. **Configure the Chart**:
   - Drag `sentiment` to the **Group by** field.
   - Drag any measurable field (e.g., `feedbackId`) to the **Value** field, ensuring it is aggregated as a count.
3. **Customize the Chart**:
   - Set the title to **"Proportion of Sentiments"**.
   - Adjust color palettes and labels as needed.

### Example 2: Sentiments Per Month (Stacked Bar Chart)
1. **Add a Visual**:
   - Click **Add visual** and select **Vertical Stacked Bar Chart**.
2. **Configure the Chart**:
   - Drag `month` to the **X-axis** field.
   - Drag `feedbackId` to the **Value** field, ensuring it is aggregated as a count.
   - Drag `sentiment` to the **Color** field for grouping.
3. **Customize the Chart**:
   - Set the title to **"Sentiment Trends by Month"**.
   - Rotate the X-axis labels for readability.

### Example 3: Sentiments by Categories for One Month (Filtered Bar Chart)
1. **Add a Visual**:
   - Click **Add visual** and select **Vertical Stacked Bar Chart**.
2. **Configure the Chart**:
   - Drag `feedbackCategory` to the **X-axis** field.
   - Drag `feedbackId` to the **Value** field, aggregated as a count.
   - Drag `sentiment` to the **Color** field for grouping.
3. **Add a Filter**:
   - Click **Add** > **Add filter**.
   - Select the `month` field.
   - Set the filter to include a specific month (e.g., `5` for May).
4. **Customize the Chart**:
   - Set the title to **"Sentiments by Category (May)"**.

### Example 4: Sentiment Proportion within a Category (Pie Chart)
1. **Add a Visual**:
   - Click **Add visual** and select **Pie Chart**.
2. **Configure the Chart**:
   - Drag `sentiment` to the **Group by** field.
   - Drag `feedbackId` to the **Value** field, aggregated as a count.
3. **Add a Filter**:
   - Click **Add** > **Add filter**.
   - Select the `feedbackCategory` field.
   - Set the filter to include a specific category (e.g., `App`).
4. **Customize the Chart**:
   - Set the title to **"Sentiment Proportion in App Category"**.