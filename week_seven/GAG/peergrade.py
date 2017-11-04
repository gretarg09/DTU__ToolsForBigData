from mrjob.job import MRJob
from mrjob.step import MRStep

class MRTotal(MRJob):
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_orders,
                reducer=self.reducer_total),
            MRStep(
                mapper=self.mapper_key,
                reducer=self.reducer_output),
        ]

    # Step 1
    def mapper_orders(self, _, line):
        (customerID, itemID, orderAmount) = line.split(',')
        yield customerID, float(orderAmount)

    def reducer_total(self, customer, orders_amount):
        yield customer, sum(orders_amount)

    # Step 2
    def mapper_key(self, customer, total_amount):
        yield '%04.02f' % float(total_amount), customer

    def reducer_output(self, orders_amount, customer):
        for user in customer:
            yield user, orders_amount


if __name__ == '__main__':
    MRTotal.run()