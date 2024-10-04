const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function weekdays(config) {
    var cfg = config || {};
    var count = cfg.count || 7;
    var values = [];
    var i, value;

    const today = new Date().getDay();

    for (i = 0; i < count; ++i) {
        value = WEEKDAYS[Math.abs((today - count + i + 8) % 7)];
        values.push(value);
    }

    return values;
}

const MONTHS = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
];

export function months(config) {
    var cfg = config || {};
    var count = cfg.count || 12;
    var section = cfg.section;
    var values = [];
    var i, value;

    const thisMonth = new Date().getMonth();

    for (i = 0; i < count; ++i) {
        value = MONTHS[Math.abs((thisMonth - count + i + 13) % 12)];
        values.push(value.substring(0, section));
    }

    return values;
}
