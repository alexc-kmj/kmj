<?php

//modified by AC
//duplicate sku detection

require_once '../public_html/app/Mage.php';
umask(0);
Mage::app ()->setCurrentStore(Mage_Core_Model_App::ADMIN_STORE_ID);
//Used to Update Titles in Bulk
$csv = array_map('str_getcsv', file('TRX_Titles_0119.csv'));
array_shift($csv);
$count = 0;
$duplicateSku = 0;
$duplicateTitle = 0;
$oldSku = "";
$oldTitle = "";

foreach($csv as $row)
{
	$sku = Mage::getModel('catalog/product')->loadByAttribute('sku', $row[0]);
	$workingSku = $row[0];
	
	if($sku)
	{
		if($oldSku == $workingSku){
			
			echo "**** duplicate sku **** \r\n";
			//echo "**** SKU: ". $workingSku . "\r\n";
			//echo "**** Title: ". $product . "\r\n";
			$duplciateSku++;
		}else{
			
			$new = $row[1];
			$product = $sku->getName();
			
			if($new == $product){
				echo "**** duplicate title **** \r\n";
				//echo "**** SKU: ". $workingSku . "\r\n";
				//echo "**** Title: ". $product . "\r\n";
				$duplicateTitle++;
				$oldSku = $workingSku;
			}else{
				echo "SKU: ". $workingSku . "\r\n";
				echo "Old Title: ". $product . "\r\n";
				echo "New Title: ". $new . "\r\n";
				//echo $new . "\r\n";
				
				$sku->setName($new);
				$sku->save();
				$count++;	
			
				$oldSku = $workingSku;
			}			
		}
	}
}

echo $count . " Products Updated" . "\r\n";
echo $duplicateSku . " Duplicate sku(s)" . "\r\n";
echo $duplicateTitle . " Duplicate Title(s)" . "\r\n";
echo "done". "\r\n";
?>