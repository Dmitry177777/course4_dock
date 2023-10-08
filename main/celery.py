# import datetime
#
# # Предположим, что self.last_execution содержит дату последнего выполнения
# # self.periodicity содержит периодичность в днях
#
# # Получаем текущую дату
# current_date = datetime.datetime.now().date()
#
# # Проверяем, была ли последняя выполненная дата
# if self.last_execution is not None:
#     # Вычисляем разницу между текущей датой и последней выполненной датой
#     days_since_last_execution = (current_date - self.last_execution).days
#
#     if days_since_last_execution < 7:
#         raise ValidationError("Действие нельзя выполнять чаще, чем раз в 7 дней.")
