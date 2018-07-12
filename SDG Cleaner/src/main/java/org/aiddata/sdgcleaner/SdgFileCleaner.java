package org.aiddata.sdgcleaner;

import org.apache.poi.openxml4j.opc.OPCPackage;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Iterator;

public class SdgFileCleaner {

    public static void main(String[] args){
        //File was broken into two parts because this wouldn't even run when it was just one file.
        File excelFileOne = new File("C:\\Users\\ry ry\\Desktop\\ML Internship\\classifier1\\sdg-autocoder\\data\\sdg_master_unique_multiple_codes.xlsx");
        File outputFile = new File("C:\\Users\\ry ry\\Desktop\\ML Internship\\classifier1\\sdg-autocoder\\data\\sdg_master_unique_cleaned.xlsx");
        try {
            ArrayList<String> stringsToPrint = new ArrayList<>();
            String newLine = System.getProperty("line.separator");

            stringsToPrint = addToList(stringsToPrint, excelFileOne, newLine);

            FileWriter fileWriter = new FileWriter(outputFile);
            fileWriter.write("title,short_description,long_description,sdg_codes" + newLine);
            for(String stringToPrint:stringsToPrint)
            {
                fileWriter.write(stringToPrint);
            }
            fileWriter.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    private static ArrayList<String> addToList(ArrayList<String> arrayList, File fileName, String newLine) throws Exception{
        OPCPackage opcPackage = OPCPackage.open(fileName);
        XSSFWorkbook workbook = new XSSFWorkbook(opcPackage);
        Iterator<Sheet> sheetIterator = workbook.sheetIterator();
        while(sheetIterator.hasNext()){
            Sheet sheet = sheetIterator.next();
            Iterator<Row> rowIterator = sheet.rowIterator();
            while(rowIterator.hasNext()){
                Row row = rowIterator.next();

                //Title Column
                Cell titleCell = row.getCell(0);
                String title = titleCell.getStringCellValue();

                //Short Description Column
                Cell shortCell = row.getCell(1);
                String shortDescription = shortCell.getStringCellValue();

                //Long Description Column
                Cell longCell = row.getCell(2);
                String longDescription = longCell.getStringCellValue();

                if(title.equals(shortDescription) && shortDescription.equals(longDescription)) {
                    continue;
                }

                /*
                //Year Column
                int year;
                Cell yearCell = row.getCell(2);
                if(yearCell != null && yearCell.getCellTypeEnum() == CellType.NUMERIC){
                    year = new Double(yearCell.getNumericCellValue()).intValue();
                    //The quotation marks around each field are because some of the fields have commas in them
                } else {
                    continue;
                }

                //Donor Column
                Cell donorCell = row.getCell(3);
                String donor = donorCell.getStringCellValue();

                //Recipient Column
                Cell recipientCell = row.getCell(4);
                String recipient = recipientCell.getStringCellValue();

                int crn_sector_code;
                Cell crnSectorCell = row.getCell(9);
                if(crnSectorCell != null && crnSectorCell.getCellTypeEnum() == CellType.NUMERIC){
                    crn_sector_code = new Double(crnSectorCell.getNumericCellValue()).intValue();
                    //The quotation marks around each field are because some of the fields have commas in them
                } else {
                    continue;
                }

                int crn_purpose_code;
                Cell crnPurposeCell = row.getCell(11);
                if(crnPurposeCell != null && crnPurposeCell.getCellTypeEnum() == CellType.NUMERIC){
                    crn_purpose_code = new Double(crnPurposeCell.getNumericCellValue()).intValue();
                    //The quotation marks around each field are because some of the fields have commas in them
                } else {
                    continue;
                }

                */
                String dnc = "DNC";
                //SDG Code Column
                Cell sdgCell = row.getCell(3);
                String finalProduct;
                if(sdgCell != null && sdgCell.getCellTypeEnum() == CellType.NUMERIC){
                    int sdgValue = new Double(sdgCell.getNumericCellValue()).intValue();
                    //The quotation marks around each field are because some of the fields have commas in them
                    finalProduct = "\"" + title + "\",\"" + shortDescription + "\",\"" + longDescription + "\"," + sdgValue + newLine;
                } else if (sdgCell != null && sdgCell.getCellTypeEnum()==CellType.STRING){

                    String sdgValue = sdgCell.getStringCellValue();

                    System.out.printf("DNC class found with code: %s\n", sdgValue);

                    if(sdgValue.equals("DNC")){
                        System.out.printf("success\n")
                        finalProduct = "\"" + title + "\",\"" + shortDescription + "\",\"" + longDescription + "\"," + sdgValue + newLine;
                    } else {
                        System.out.printf("%s code not equal to 'DNC'\n", sdgValue);
                        continue;
                    }

                } else {
                    continue;
                }
                if(!arrayList.contains(finalProduct)){
                    arrayList.add(finalProduct);
                }
            }
        }
        return arrayList;
    }
}
