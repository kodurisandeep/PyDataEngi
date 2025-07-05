from hmac import new
import xml.etree.ElementTree as ET

# 🧾 Load and parse the XML file
tree = ET.parse("./dataset_samples/D4_Employees.xml")
root = tree.getroot()

print("Root tag:", root.tag)

# 🌿 Loop through <employee> tags
for emp in root.findall("employee"):
    emp_id = emp.get("id")  # Attribute

    # Extract sub-elements safely (handles missing tags)
    name_tag = emp.find("name")
    dept_tag = emp.find("department")
    loc_tag  = emp.find("location")

    name = name_tag.text if name_tag is not None else "N/A"
    dept = dept_tag.text if dept_tag is not None else "N/A"
    loc  = loc_tag.text  if loc_tag  is not None else "N/A"

    # Extract nested attribute example: <name title="Manager">Ravi</name>
    title = name_tag.get("title") if name_tag is not None and "title" in name_tag.attrib else "Unknown"

    print(f"{emp_id}: {name} ({title}), {dept}, {loc}")

# 🔍 Example: XPath-style filtering — find specific employee by ID
target_emp = root.findall(".//employee[@id='E002']")
if target_emp:
    name = target_emp[0].find("name").text
    print(f"XPath Match - E002: {name}")

# 📦 Read from XML string (optional test)
xml_string = """
<employee id="E003">
    <name title="Intern">Farhan</name>
    <department>Tech</department>
</employee>
"""
tree_from_string = ET.ElementTree(ET.fromstring(xml_string))
emp_node = tree_from_string.getroot()
print("Parsed from string:", emp_node.find("name").text)

# 🛠️ Create and write a new XML
new_emp = ET.Element("employee", id="E004")
ET.SubElement(new_emp, "name", title="Lead").text = "Kiran"
ET.SubElement(new_emp, "department").text = "Finance"
ET.SubElement(new_emp, "location").text = "Pune"

new_tree = ET.ElementTree(new_emp)
new_tree.write("./dataset_samples/D4_New_employee.xml", encoding="utf-8", xml_declaration=True)
print("New XML file written: new_employee.xml")

root.append(new_emp)
# Write the updated tree back to the same file
tree.write("./dataset_samples/D4_Employees2.xml", encoding="utf-8", xml_declaration=True)
print("New employee appended to XML file!")
