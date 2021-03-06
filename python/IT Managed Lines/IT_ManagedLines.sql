SELECT
	  plc.PLC + ' ' +	p.PartNumber as "sku", 
	CASE
		WHEN FLOOR(IFNULL(p.OnHand, 0) - (IFNULL(coo.CommittedOnOrders, 0) + IFNULL(ohc.OnHoldForConversion, 0) + IFNULL(ohb.OnHoldForBackorders, 0))) < 0 THEN 0
		ELSE FLOOR(IFNULL(p.OnHand, 0) - (IFNULL(coo.CommittedOnOrders, 0) + IFNULL(ohc.OnHoldForConversion, 0) + IFNULL(ohb.OnHoldForBackorders, 0)))
	END as "quantity", p.RecDate
FROM Plc plc
	 INNER JOIN Imaster p ON plc.PLCID = p.PLCID
	 LEFT JOIN
	 (
	  	  SELECT
	  		oi.PartID,
	  		SUM(oi.Shipped) AS CommittedOnOrders
	  	  FROM SalesOrder so
	  	  	 INNER JOIN [Order] o on so.OrderNumber = o.OrderNumber
	  	  	 INNER JOIN OrderItem oi ON o.OrderNumber = oi.OrderNumber
	  	  WHERE o.OrderOpen = TRUE
	  	  	 AND oi.LineType <> 'X'
	  	  	 AND (oi.IsDropShipping IS NULL OR oi.IsDropShipping = FALSE)
	  	  	 AND o.OrderType <> 'F'
	  	  	 AND oi.Shipped > 0
	  	  GROUP BY oi.PartID
	 ) coo ON p.PartID = coo.PartID
	 LEFT JOIN
	 (
	  	  SELECT
	  		oi.xPartID,
	  		SUM(oi.Shipped) AS OnHoldForConversion
	  	  FROM SalesOrder so
	  	  	 INNER JOIN [Order] o on so.OrderNumber = o.OrderNumber
	  	  	 INNER JOIN OrderItem oi ON o.OrderNumber = oi.OrderNumber
	  	  WHERE o.OrderOpen = TRUE
	  	  	 AND oi.LineType = 'X'
	  	  	 AND o.OrderType <> 'F'
	  	  	 AND oi.Shipped > 0
	  	  GROUP BY oi.xPartID
	 ) ohc ON p.PartID = ohc.xPartID
	 LEFT JOIN
	 (
	  	  SELECT
	  		b.PartID,
	  		SUM(b.QtyOnBO) AS QtyOnBO
	  	  FROM Backorders b
	  	  GROUP BY b.PartID
	 ) qob ON p.PartID = qob.PartID
	 LEFT JOIN
	 (
	  	  SELECT
	  		b.PartID,
	  		SUM(b.QtyHeld) AS OnHoldForBackorders
	  	  FROM Backorders b
	  	  GROUP BY b.PartID
	 ) ohb ON p.PartID = ohb.PartID
	 LEFT JOIN
	 (
	  	  SELECT
	  		oi.PartID,
	  		SUM(IFNULL(oi.Ordered, 0) - (IFNULL(oi.Shipped, 0) + IFNULL(r.Received, 0))) AS OnOrder
	  	  FROM PurchaseOrder po
	  	  	 INNER JOIN [Order] o on po.OrderNumber = o.OrderNumber
	  	  	 INNER JOIN OrderItem oi ON o.OrderNumber = oi.OrderNumber
			 LEFT JOIN
			 (
			  	   SELECT
				   		 irj.OrderLineID,
						 SUM(irj.Qty) AS Received
				   FROM InventoryReceiptsJrnl irj
				   GROUP BY irj.OrderLineID
			 ) r ON oi.OrderLineID = r.OrderLineID
	  	  WHERE o.OrderOpen = TRUE
		  	 AND po.POStatus <> 'PENDING ORDER'
	  	  	 AND (oi.IsDropShipping IS NULL OR oi.IsDropShipping = FALSE)
	  	  GROUP BY oi.PartID
	 ) oo ON p.PartID = oo.PartID
WHERE p.RecordActive = TRUE AND p.ItemIsKit = FALSE
	  AND p.RecDate = '2018-03-31'
	  AND (p.ExportToEbay = 1 OR p.ExportToAmazon = 1 OR p.Is_On_Magento = TRUE)
	  AND (PLC.PLC = 'GFU' OR PLC.PLC = 'FMP' OR PLC.PLC = 'AVS' OR PLC.PLC = 'BLM' OR PLC.PLC = 'BUS' OR PLC.PLC = 'LND' 
	  	  OR PLC.PLC = 'RPG' OR PLC.PLC = 'RNL' OR PLC.PLC = 'STA' OR PLC.PLC = 'FLO' OR PLC.PLC = 'BMM' OR PLC.PLC = 'HUR')
ORDER BY plc.PLC, p.PartNumber;