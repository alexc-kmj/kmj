<?php
	require_once '../public_html/app/Mage.php';
	umask(0);
	Mage::app()->setCurrentStore(Mage_Core_Model_App::ADMIN_STORE_ID);
	
	//Edit file name, make sure it is comma delimited.
	$csv = array_map('str_getcsv', file('SpecialPrice.csv'));
	
	$updated = 0;
	$not_updated = 0;
	$same_price = 0;
	$previousSKU = "";
	$special_price = 0;
	$count_SameSKU = 0;
	
	$products_updated = array();
	$product_notupdated = array();
	
	$plc_map = array('ACC', 'AMP', 'ARA', 'BMM', 'BRG', 'BRU', 'BUS', 'EIB', 'FIT', 'FLE', 'FLO', 'FST', 'GFS', 'GFU', 'GRF', 'HSK', 'HUR', 'HYT', 'KNN', 'MDN',
		'MSD', 'PRO', 'QUI', 'RAC', 'RDL', 'RNL', 'TIM', 'TRX');
	
	foreach ( $csv as $row ) {
		$product = Mage::getModel('catalog/product')->loadByAttribute('sku', $row[0]);
		
		$plc = substr($row[0], 0, 3);
		$partnumber = substr($row[0], 4);
		
		if ( $product ) {			
			if ( $previousSKU == $row[0] ) {
				//echo "Same SKU: " . $row[0] . "\r\n";
				$count_SameSKU++;
			} elseif ( floatval($row[1]) === floatval($product->getPrice()) ) {
				$same_price = $same_price + 1;
			} elseif ( in_array($plc, $plc_map)) {
				if ( floatval($row[1]) < floatval($product->getPrice()) ){
					echo 'Updating Speical Price: ' . $row[0] . ' -> ' . $product->getSpecialPrice . ' to ' . $row[1];
					echo "\r\n";
					
					$product->setSpecialPrice($row[1]);
					$product->save();
					$special_price += 1;
				}
			} else {	
				if ( $plc == 'AFE' || $plc == 'PUT' || $plc == 'GFS' ){
					//Do nothing to special price
					echo 'Updating Price: ' . $row[0] . ' -> ' . $product->getPrice . ' to ' . $row[1];
					echo "\r\n";
					
					$product->setPrice($row[1]);
					$product->save();
					$updated = $updated + 1;
					array_push($products_updated, $row[0]);
					
				} else {
					
					echo 'Updating Price: ' . $row[0] . ' -> ' . $product->getPrice . ' to ' . $row[1];
					echo "\r\n";
					
					$product->setPrice($row[1]);
					$product->setSpecialPrice();
					$product->save();
					$updated = $updated + 1;
					array_push($products_updated, $row[0]);
				}
			}
			$previousSKU = $row[0];
		} else {
			$not_updated = $not_updated + 1;
			array_push($product_notupdated, $row[0]);
		}
	}
	
	echo "\r\n";
	echo "Updated: " . $updated . "\r\n";
	echo "Not Updated: " . $not_updated . "\r\n";
	echo "Special Price: " . $special_price . "\r\n";
	echo "Product Prices Same After Updating " . $same_price . "\r\n"; 
	
	echo "Same SKU: " . $count_SameSKU . "\r\n";
	echo "Updated" . "\r\n";
	echo "-----------" . "\r\n";
	
	foreach( $products_updated as $sku ) {
		echo $sku . "\r\n";
	}
	echo "\r\n";
	
	echo "Not Updated\r\n";
	echo "-----------\r\n";
	foreach($product_notupdated as $sku)
	{
		echo $sku . "\r\n";
	}
?>