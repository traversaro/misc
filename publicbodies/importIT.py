#!/usr/bin/python3

import urllib.request
import csv
import datetime

#ipa -> indicePa , pbo -> publicbodies.org
IPA_FILENAME = "amministrazioni.txt"
PBO_FILENAME = "it.csv"

#metadata documentation: http://www.indicepa.gov.it/public-services/docs-read-service.php?dstype=FS&filename=Metadati_Open_Data.pdf
ipa_fieldnames = ["cod_amm","des_amm","Comune","nome_resp","cogn_resp","Cap","Provincia","Regione","sito_istituzionale","Indirizzo","titolo_resp","tipologia_istat","Acronimo","cf_validato","Cf","mail1","tipo_mail1","mail2","tipo_mail2","mail3","tipo_mail4","mail5","tipo_mail5","url_facebook","url_twitter","url_googleplus","url_youtube","liv_accessibili"]
pbo_fieldnames = ["title","abbr","key","category","parent","parent_key","description","url","jurisdiction","jurisdiction_code","source","source_url","address","contact","email","tags","created_at","updated_at"]

def download_indicepa():
    URL = "http://www.indicepa.gov.it/public-services/opendata-read-service.php?dstype=FS&filename=amministrazioni.txt"
    print("Downloading indicePA data")
    file_req = urllib.request.urlopen(URL)
    print("indicePA data downloaded, saving to "+IPA_FILENAME)
    output = open(IPA_FILENAME,'wb')
    output.write(file_req.read())
    output.close()
    print("indicePA data saved")
    
def convert_data():
    pbo_writer = csv.DictWriter(open(PBO_FILENAME, 'w', newline=''), fieldnames=pbo_fieldnames, delimiter=',')
    pbo_writer.writeheader()
    with open(IPA_FILENAME) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(10000))
        csvfile.seek(0)
        ipa_reader = csv.DictReader(csvfile,fieldnames=ipa_fieldnames,dialect=dialect)
        for ipa_row in ipa_reader:
            #clean row from "null" values
            for key in ipa_row.keys():
                if ipa_row[key] == "null":
                    ipa_row[key] = ""
            
            
            pbo_row = {}
            print("Saving PB " + ipa_row["cod_amm"])
            pbo_row["title"] = ipa_row["des_amm"]
            pbo_row["abbr"] = ipa_row["Acronimo"]
            pbo_row["key"] = "it/" + ipa_row["cod_amm"]
            pbo_row["category"] = ""
            pbo_row["parent"] = ""
            pbo_row["parent_key"] = ""
            pbo_row["description"] = ""
            pbo_row["url"] = ipa_row["sito_istituzionale"]
            pbo_row["jurisdiction"] = "Italy"
            pbo_row["jurisdiction_code"] = "IT"
            pbo_row["source"] = "Indice delle Pubbliche Amministrazioni"
            pbo_row["source_url"] = "http://www.indicepa.gov.it/ricerca/dettaglioamministrazione.php?cod_amm=" + ipa_row["cod_amm"]
            pbo_row["address"] = ipa_row["Indirizzo"].replace(","," ") + " - " + ipa_row["Cap"] + " " + ipa_row["Comune"] + " (" + ipa_row["Provincia"] + ") " + "Italy" 
            pbo_row["contact"] = ""
            pbo_row["email"] =  ipa_row["mail1"]
            pbo_row["tags"] = ""
            pbo_row["created_at"] = datetime.datetime.now().date().isoformat()
            pbo_row["updated_at"] = datetime.datetime.now().date().isoformat()                                   
            pbo_writer.writerow(pbo_row)


download_indicepa()
convert_data()
