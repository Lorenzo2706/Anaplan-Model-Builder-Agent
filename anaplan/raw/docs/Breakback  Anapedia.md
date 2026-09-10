---
title: "Breakback | Anapedia"
source: "https://help.anaplan.com/breakback-1b7aa87d-aa13-49f6-8f7d-d893fb8bccbe"
author:
published:
created: 2026-09-03
description: "Breakback lets you type a value into a total (aggregate) cell, and all the cell values that make up the total are changed to reflect the total value. For example, you can distribute a total annual salary over 12 months to calculate a monthly payment. Breakback is indicated by a blue triangle in the top-left corner of the cell."
tags:
  - "clippings"
---
Breakback lets you type a value into a total (aggregate) cell, and all the cell values that make up the total are changed to reflect the total value. For example, you can distribute a total annual salary over 12 months to calculate a monthly payment. Breakback is indicated by a blue triangle in the top-left corner of the cell.

You can use Breakback to allocate data using seasonality patterns. For example, you could specify a profile based on expected sales throughout a year, then enable Breakback. When you type a value into the total, data is allocated across the cells pro-rata.

[Enable Breakback](https://help.anaplan.com/38ca581f-2e20-4bc7-9a27-9f4ce13f485d) in **Modules** in the model settings bar, or in the module's Blueprint.

This example contains seasonality data loaded into a grid, with **Breakback** enabled for the *Gross Sales* line item.

![This is a grid with Gross sales selected on Pages, Time on Columns, and Organization on Rows. Breakback is enabled, indicated by a blue triangle in the top left corner of the cells in the Q1 FY22 column.](https://assets-us-01.kc-usercontent.com/cddce937-cf5a-003a-bfad-78b8fc29ea3f/124c9d6f-3cda-4985-850d-4647a6373b4d/Breakback%20example.jpg)

If you change the *Q1 FY2022* total for *Belfast* to 6,000, breakback is triggered. Data is allocated across the months and regions pro rata based on the original values. The UK figures are also updated to reflect this.

![This is a grid with Gross sales selected on Pages, Time on Columns, and Organization on Rows. This grid shows the impact of Breakback on the Belfast row. 6000 was entered into Q1 FY22, and the data in Jan 22, Feb 22, Mar 22 was updated proportionately to reflect the total of 6000.](https://assets-us-01.kc-usercontent.com/cddce937-cf5a-003a-bfad-78b8fc29ea3f/9eb28ff6-97e1-43d6-85e5-9e798e00eca5/Breakback%20example%202.jpg)

Breakback works across multiple dimensions. For example, if you change the **Q1 FY22** total for the UK, breakback uses the seasonality pattern to allocate across months, and the geographical split to allocate across the cities.

**Note:** If a Breakback change to a lower-level item in a [list hierarchy](https://help.anaplan.com/2fc52da8-b161-4d29-acfb-9aafde1b5bae) affects cell data for a higher-level item, the change only displays in the [cell history](https://help.anaplan.com/a8a937d8-5423-44a8-94c7-7776b4626790) for the lower-level item.

If the sum of the cells in a grid is zero, typing a value into a total allocates the amount evenly across the leaf-level cells. In this example, 12,000 is typed into Q1 FY22 and is allocated evenly across the three months.

|  | **Jan 22** | **Feb 22** | **Mar 22** | **Q1 FY22** |
| --- | --- | --- | --- | --- |
| Germany | 4,000 | 4,000 | 4,000 | 12,000 |

You can copy and paste into several Breakback-enabled totals at once. All child cells affected by each Breakback total are updated accordingly for the change in total values.

Total cells that have Breakback enabled have a blue triangle in the top-left corner. Hover over the Breakback marker to see how many cells are impacted by Breakback. You can hide the Breakback markers in the Help menu. Select **Hide breakback markers**.

Breakback can affect many cells. Because of this, the [change history](https://help.anaplan.com/1af91b89-11bb-4c58-9ca6-cbe7ca8a9275) for a module only shows the cell change that originally triggered the Breakback, together with the total number of affected cells.

[**Hold**](https://help.anaplan.com/50120833-168b-42d6-a773-6523bb89566d) is a Breakback feature that allows you to temporarily 'hold' values in cells. Use **Hold** to update totals without impacting a value for a line item, or to change values for a particular line item without changing the overall total.

Read-only cells are held at their previous values when Breakback is triggered. The cells could be read-only because of [Selective Access](https://help.anaplan.com/f0dd364d-cd04-429e-b788-15c79d8cf698) settings, or because of [Dynamic Cell Access](https://help.anaplan.com/55ae93e6-5139-4bbf-93f9-c8cb06f68f75) settings. Cells can also be read-only in a rolling forecast, where early months contain historical data that can't be changed.

Breakback doesn't work in all cases. For example, if you have leaf-level cells that don't contain zeros that sum up to a zero total, as shown in this example, an error is displayed.

|  | **Jan 22** | **Feb 22** | **Mar 22** | **Q1 FY22** |
| --- | --- | --- | --- | --- |
| Berlin | \-1,178 | 589 | 589 | 0 |

Breakback isn't permitted across several line items. It's restricted to totals on simple hierarchies and totals on the time dimension.

If the use of Breakback affects more than 1,000,000 cells, then the system displays a warning message.

<iframe title="Feedback Survey" src="https://nebula-cdn.kampyle.com/us/md-form/website/1.25.2/index.html?formId=32270&amp;type=live&amp;isMobile=false&amp;device=desktop&amp;referrer=https%3A%2F%2Fhelp.anaplan.com%2Fbreakback-1b7aa87d-aa13-49f6-8f7d-d893fb8bccbe&amp;region=digital-cloud-us-main&amp;displayType=embedded&amp;isSeparateFormTemplateFromData=true&amp;domainsListRelativePath=..%7C..%7C..%7C..%7Cus%2Fwu%2F568549%2Fonsite"></iframe>