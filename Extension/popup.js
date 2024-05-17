document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const selectFilesButton = document.getElementById('selectFilesButton');
    const browseFiles = document.getElementById('browseFiles');
    const piiSections = document.getElementById('piiSections');
    const scanButton = document.getElementById('scanButton');
    const statisticsSection = document.getElementById('statisticsSection');
    const downloadButton = document.getElementById('downloadButton');

    const namesCount = document.getElementById('namesCount');
    const emailsCount = document.getElementById('emailsCount');
    const phonesCount = document.getElementById('phonesCount');
    const addressesCount = document.getElementById('addressesCount');
    const birthdatesCount = document.getElementById('birthdatesCount');
    const medicalInfoCount = document.getElementById('medicalInfoCount');

    dropZone.addEventListener('click', () => fileInput.click());
    browseFiles.addEventListener('click', () => fileInput.click());
    selectFilesButton.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        fileInput.files = e.dataTransfer.files;
        handleFiles(fileInput.files);
    });

    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            selectFilesButton.style.display = 'none';
            piiSections.style.display = 'block';
        }
    }

    scanButton.addEventListener('click', () => {
        // Simulate scanning the file and show PII statistics
        showStatistics({
            names: 2,
            emails: 1,
            phones: 2,
            addresses: 6,
            birthdates: 1,
            medicalInfo: 4
        });
    });

    function showStatistics(stats) {
        piiSections.style.display = 'none';
        statisticsSection.style.display = 'block';

        namesCount.textContent = stats.names;
        emailsCount.textContent = stats.emails;
        phonesCount.textContent = stats.phones;
        addressesCount.textContent = stats.addresses;
        birthdatesCount.textContent = stats.birthdates;
        medicalInfoCount.textContent = stats.medicalInfo;
    }

    downloadButton.addEventListener('click', () => {
        const link = document.createElement('a');
        link.href = '/mnt/data/Redact PII-65ea9b5559888d39757f10fd-data 2.pdf';  // Make sure the file path is correct
        link.download = 'Redact_PII_Data.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    document.querySelectorAll('.pii-category h2').forEach(sectionHeader => {
        sectionHeader.addEventListener('click', () => {
            const form = sectionHeader.nextElementSibling;
            form.style.display = form.style.display === 'block' ? 'none' : 'block';
        });
    });
});
